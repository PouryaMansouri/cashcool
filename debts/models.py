import calendar
import math
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.db import models, transaction as db_transaction
from django.db.models import Sum

from base_everything.constants import LOWER_BASE_CASHTAG
from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.credit_transactions.models import CreditTransaction
from credit_card.debts.constants import DEBT_STATUS_CHOICES, DEBT_PENALTY_STATUS_CHOICES, BANK_PENALTY_RATE
from cwallets.models import CWalletRegular
from transactions.internal_app_requests import execute_tx_request_from_another_app
from transactions.models import TransactionRegular
from .exceptions import BadDebtCreditTransactionObject, BadDebtRepaymentCreditTransactionObject, RepaymentMoreThanDebt, \
    ThisDebtPenaltyCreateRepetitive


class Debt(models.Model):
    credit_cwallet = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE, related_name="user_credit_cwallet")
    credit_transaction = models.ForeignKey(CreditTransaction, on_delete=models.CASCADE)
    status = models.IntegerField(choices=DEBT_STATUS_CHOICES, default=DEBT_STATUS_CHOICES.not_payed)
    repayment_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debt"

    def __str__(self):
        return "{} | {} | {} ".format(self.credit_cwallet.current_cashtag.cashtag,
                                      self.credit_transaction.id,
                                      self.credit_transaction.ptc)

    @property
    def debt_remain(self):
        debt_remain = DebtHistory.objects.filter(
            debt_credit_cwallet=self).aggregate(Sum('amount'))
        return debt_remain['amount__sum']

    @property
    def all_debt_remain(self):
        all_debt_remain = DebtHistory.objects.filter(
            debt_credit_cwallet__credit_cwallet=self.credit_cwallet).aggregate(Sum('amount'))

        penalty_remain = DebtPenalty.objects.filter(
            debt__credit_cwallet=self.credit_cwallet, status=DEBT_STATUS_CHOICES.not_payed).aggregate(
            Sum('penalty_amount'))
        if penalty_remain['penalty_amount__sum']:
            all_debt_remain = all_debt_remain['amount__sum'] + penalty_remain['penalty_amount__sum']
            return all_debt_remain
        else:
            return all_debt_remain['amount__sum']
        # return all_debt_remain['amount__sum']

    def calculate_debt_datetime(self):
        first_not_pay_transaction = Debt.objects.filter(credit_cwallet=self.credit_cwallet,
                                                        status=DEBT_STATUS_CHOICES.not_payed).order_by(
            'created_at').first()
        # TODO calculate based on jalali date time. it means if value is jalali
        now = datetime.utcnow()
        if first_not_pay_transaction:
            check_time = datetime(year=first_not_pay_transaction.year, month=first_not_pay_transaction.month,
                                  day=first_not_pay_transaction.day)
        else:
            check_time = datetime(year=now.year, month=now.month, day=now.day)
        if now <= check_time:
            debt_datetime = check_time + relativedelta(months=+1)
            debt_datetime = debt_datetime.replace(hour=23, minute=59, second=59)
        else:
            debt_datetime = check_time
            debt_datetime = debt_datetime.replace(hour=23, minute=59, second=59)

        return debt_datetime

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.repayment_date_time = self.calculate_debt_datetime()
        return super(Debt, self).save(force_insert=False, force_update=False, using=None,
                                      update_fields=None)


class DebtHistory(models.Model):
    '''
    debt amount is negative
    repayment is positive
    '''

    debt_credit_cwallet = models.ForeignKey(Debt, on_delete=models.CASCADE,
                                            related_name="debt_transaction")
    repayment_debt_transaction = models.ForeignKey(TransactionRegular, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debt_history"

    def __str__(self):
        return "{} | {} | {} | {} ".format(self.debt_credit_cwallet.credit_cwallet.current_cashtag.cashtag,
                                           self.debt_credit_cwallet.credit_transaction.id,
                                           self.repayment_debt_transaction,
                                           self.debt_credit_cwallet.credit_transaction.ptc)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.repayment_debt_transaction:
            if self.amount >= 0:
                raise BadDebtCreditTransactionObject

        if self.repayment_debt_transaction:
            if self.amount <= 0:
                raise BadDebtRepaymentCreditTransactionObject

            previous_debt_history_amount_sum = DebtHistory.objects.filter(
                debt_credit_cwallet=self.debt_credit_cwallet).aggregate(Sum('amount'))
            previous_debt_history_amount_sum = previous_debt_history_amount_sum['amount__sum']
            # TODO chera khate payin be hich jash nist va pashmeshe? too avalin debt history
            if not previous_debt_history_amount_sum:
                return super(DebtHistory, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)

            if self.amount > abs(previous_debt_history_amount_sum):
                raise RepaymentMoreThanDebt

        return super(DebtHistory, self).save(force_insert=False, force_update=False, using=None,
                                             update_fields=None)


class DebtRepayment:
    @staticmethod
    def do_repayment(credit_cwallet: CreditCwallet, cwallet: CWalletRegular, amount: Decimal, context, request):
        debts = Debt.objects.filter(credit_cwallet=credit_cwallet,
                                    status=DEBT_STATUS_CHOICES.not_payed).order_by('created_at')
        all_remain_debt = debts.first().all_debt_remain
        if amount > debts.first().all_debt_remain:
            amount = debts.first().all_debt_remain

        with db_transaction.atomic():
            # 1. create transaction between cwallet of user and CashCool main CWallet
            repayment_transaction = execute_tx_request_from_another_app(context, request, sender=cwallet,
                                                                        receiver_cashtag=LOWER_BASE_CASHTAG,
                                                                        amount=amount)
            # 2. create new debt history with positive amount
            for debt in debts:
                remain = debt.debt_remain
                if amount > remain:
                    DebtHistory.objects.create(debt_credit_cwallet=debt,
                                               repayment_debt_transaction=repayment_transaction,
                                               amount=remain)
                    debt.status = DEBT_STATUS_CHOICES.payed
                    debt.save()

                    amount = amount - remain
                elif amount == remain:
                    new_demand_history = DebtHistory.objects.create(demand=debt, amount=amount)
                    debt.status = DEBT_STATUS_CHOICES.payed
                    debt.save()

                    break
                elif amount < remain:
                    new_demand_history = DebtHistory.objects.create(demand=debt, amount=amount)
                    break
            # 2.5 refresh all debts object
            for debt in debts:
                debt.refresh_from_db()

            # 3 add credit amount to balance
            if debts.first().all_debt_remain == 0:
                credit_cwallet.balance = credit_cwallet.credit_amount
                credit_cwallet.save()


class DebtPenalty(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    penalty_amount = models.DecimalField(max_digits=9, decimal_places=0)
    status = models.IntegerField(choices=DEBT_PENALTY_STATUS_CHOICES, default=DEBT_PENALTY_STATUS_CHOICES.not_payed)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debt_penalty"

    def calculate_debt_penalty(self):
        now = datetime.utcnow().date()
        debt_repayment_date_time = self.debt.repayment_date_time.date()
        delta_days_between_repayment_date_time_and_now = (now - debt_repayment_date_time).days
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        debt_amount = self.debt.debt_remain
        penalty_rate = (Decimal(BANK_PENALTY_RATE) / Decimal(days_in_month))
        # ---Decimal(1) is for round up
        penalty_amount = math.ceil(
            debt_amount * penalty_rate * delta_days_between_repayment_date_time_and_now) + Decimal(-1)
        return penalty_amount

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        now = datetime.utcnow().date()
        is_penalty_create_before = DebtPenalty.objects.filter(debt=self.debt, created_at__year=now.year,
                                                              created_at__month=now.month, created_at__day=now.day)
        if is_penalty_create_before:
            raise ThisDebtPenaltyCreateRepetitive

        self.penalty_amount = self.calculate_debt_penalty()
        return super(DebtPenalty, self).save(force_insert=False, force_update=False, using=None,
                                             update_fields=None)
