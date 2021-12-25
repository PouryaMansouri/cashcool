from datetime import datetime, timedelta
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models, transaction as db_transaction
from django.utils.translation import gettext_lazy as _

from credit_card.credit_cwallets.constants import CREDIT_CWALLET_CHOICES
from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.credit_transactions.constants import TRANSACTION_STATUS_CHOICES
from credit_card.credit_transactions.signals import post_atomic_credit_transaction, \
    post_atomic_credit_transaction_for_debt_creation
# from credit_card.debts.signals import post_create_debt_after_transaction
from credit_card.demands.models import DemandHistory, Demand
from .exceptions import NotCompatibleMarketerOrganization, BadReceiverInTransaction, SenderIsBanned, ClubIsBanned, \
    TransactionWithBadCommissionData, InvalidCreditTransactionAmount, NotEnoughBalance,RepetitiveCreditTransaction


class CreditTransaction(models.Model):
    sender = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE, related_name="credit_cwallet")
    receiver = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE, related_name="club_or_credit_cwallet")
    amount = models.DecimalField(max_digits=9, decimal_places=0, validators=[MinValueValidator(1)])

    ptc = models.CharField(max_length=256)

    error_explanation = models.TextField(null=True, blank=True)

    commission_transaction = models.BooleanField(default=False)
    commission_transaction_parent = models.IntegerField(null=True, blank=True)

    status = models.IntegerField(choices=TRANSACTION_STATUS_CHOICES, default=TRANSACTION_STATUS_CHOICES.pending)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit_transaction"

    def __str__(self):
        return "{} -[{}]> {}".format(self.sender.current_cashtag.cashtag, self.amount,
                                     self.receiver.current_cashtag.cashtag)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.receiver.is_demand:
            raise BadReceiverInTransaction

        if not self.sender.credit_marketer == self.receiver.credit_marketer:
            raise NotCompatibleMarketerOrganization

        if self.sender.status == CREDIT_CWALLET_CHOICES.banned:
            raise SenderIsBanned

        if self.receiver.status == CREDIT_CWALLET_CHOICES.banned:
            raise ClubIsBanned

        if not self.commission_transaction and self.commission_transaction_parent:
            raise TransactionWithBadCommissionData

        if self.commission_transaction and not self.commission_transaction_parent:
            raise TransactionWithBadCommissionData

        # check repetitive tx
        thirty_seconds_before = datetime.utcnow() - timedelta(seconds=30)
        repetitive_tx = CreditTransaction.objects.filter(sender=self.sender,
                                                         receiver=self.receiver, amount__exact=self.amount,
                                                         created_at__gte=thirty_seconds_before,
                                                         status=TRANSACTION_STATUS_CHOICES.success)
        if repetitive_tx:
            raise RepetitiveCreditTransaction

        if not self.commission_transaction:
            if self.amount < 1000:
                raise InvalidCreditTransactionAmount

        return super(CreditTransaction, self).save(force_insert=False, force_update=False, using=None,
                                                   update_fields=None)

    def do_transaction(self, send_signal=True, send_debt=True, pay_from_demand=False):
        ptc = uuid4().hex
        try:
            with db_transaction.atomic():
                if pay_from_demand:
                    new_demand_of_sender = Demand.reduce_from_demands(self.sender, self.amount)
                else:
                    new_balance_of_sender = self.sender.reduce_credit_cwallet_balance(self.amount)

                new_demand_of_receiver = DemandHistory.add_to_demand_for_new_transaction(self.amount,
                                                                                         credit_cwallet=self.receiver,
                                                                                         credit_transaction=self)
                self.status = TRANSACTION_STATUS_CHOICES.success
                self.ptc = ptc
                self.save()

                if send_signal:
                    post_atomic_credit_transaction.send(sender=CreditTransaction, instance=self)

                if send_debt and send_signal:
                    post_atomic_credit_transaction_for_debt_creation.send(sender=CreditTransaction, instance=self)

        # TODO: use this for which Error to save error explanation in database?
        except NotEnoughBalance:
            with db_transaction.atomic():
                self.status = TRANSACTION_STATUS_CHOICES.reject
                self.error_explanation = _("sender have not enough balance.")
                self.ptc = ptc
                self.save()
            raise NotEnoughBalance
