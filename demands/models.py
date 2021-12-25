from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.db import models, transaction as db_transaction
from django.db.models import Sum

from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.demands.constans import DEMAND_STATUS, DEMANDS_HISTORIES_STATUS
from credit_card.demands_settings.constants import DEMADN_SETTING_TYPE_CHOICES
from credit_card.demands_settings.models import DemandSetting
from .exceptions import WithdrawMoreThanDebt, NotEnoughDemand


class Demand(models.Model):
    credit_cwallet = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE)
    release_datetime = models.DateTimeField()

    credit_transaction = models.ForeignKey("credit_transactions.CreditTransaction", on_delete=models.CASCADE)

    status = models.IntegerField(choices=DEMAND_STATUS, default=DEMAND_STATUS.pending)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "demand"

    def __str__(self):
        return "{} | {} | {} ".format(self.credit_cwallet.current_cashtag.cashtag,
                                      self.credit_transaction.id,
                                      self.credit_transaction.ptc)

    @property
    def demand_remain(self):
        demand_remain = DemandHistory.objects.filter(
            demand=self).aggregate(Sum('amount'))
        return demand_remain['amount__sum']

    @property
    def demand_balance(self):
        demand_remain = DemandHistory.objects.filter(
            demand__credit_cwallet=self.credit_cwallet).aggregate(Sum('amount'))
        return demand_remain['amount__sum']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.release_datetime = self.calculate_release_datetime()
        return super(Demand, self).save(force_insert=False, force_update=False, using=None,
                                        update_fields=None)

    def calculate_release_datetime(self):
        type_setting = self.credit_cwallet.demand_setting.type
        value_setting = self.credit_cwallet.demand_setting.value
        now = datetime.utcnow()
        if type_setting == DEMADN_SETTING_TYPE_CHOICES.fixed_time:
            check_time = datetime(year=now.year, month=now.month, day=value_setting)
            if now >= check_time:
                release_datetime = check_time + relativedelta(months=+1)
            else:
                release_datetime = check_time

            return release_datetime
        elif type_setting == DEMADN_SETTING_TYPE_CHOICES.period_day:
            register_time = self.credit_cwallet.created_at
            days_from_register_time = (now.date() - register_time.date()).days
            days_until_next_period = value_setting - (days_from_register_time % value_setting)
            release_datetime = now + timedelta(days=days_until_next_period)
            release_datetime = release_datetime.replace(hour=0, minute=0, second=0)

            return release_datetime

        elif type_setting == DEMADN_SETTING_TYPE_CHOICES.fixed_amount:
            pass
            # TODO get from history

    @classmethod
    def create_demand_for_new_transaction(cls, credit_cwallet, credit_transaction):
        return cls.objects.create(credit_cwallet=credit_cwallet, credit_transaction=credit_transaction)

    @classmethod
    def reduce_from_demands(cls, credit_cwallet, amount):

        demands = Demand.objects.filter(credit_cwallet=credit_cwallet, status=DEMAND_STATUS.pending).order_by(
            '-created_at')
        if amount > demands.first().demand_balance:
            raise NotEnoughDemand

        with db_transaction.atomic():
            for dm in demands:
                remain = dm.demand_remain
                if amount > remain:
                    new_demand_history = DemandHistory.objects.create(demand=dm, amount=-(remain),
                                                                      status=DEMANDS_HISTORIES_STATUS.shopping)
                    dm.status = DEMAND_STATUS.done
                    dm.save()

                    amount = amount - remain
                elif amount == remain:
                    new_demand_history = DemandHistory.objects.create(demand=dm, amount=-(amount),
                                                                      status=DEMANDS_HISTORIES_STATUS.shopping)
                    dm.status = DEMAND_STATUS.done
                    dm.save()

                    break
                elif amount < remain:
                    new_demand_history = DemandHistory.objects.create(demand=dm, amount=-(amount),
                                                                      status=DEMANDS_HISTORIES_STATUS.shopping)
                    break


class DemandHistory(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=0)
    status = models.IntegerField(choices=DEMANDS_HISTORIES_STATUS, default=DEMANDS_HISTORIES_STATUS.pay_to_club)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "demand_history"

    def __str__(self):
        return "{} | {} | {} ".format(self.demand.credit_cwallet.current_cashtag.cashtag,
                                      self.demand.credit_transaction.id,
                                      self.demand.credit_transaction.ptc)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        previous_demand_history_amount_sum = DemandHistory.objects.filter(
            demand=self.demand).aggregate(Sum('amount'))
        previous_demand_history_amount_sum = previous_demand_history_amount_sum['amount__sum']

        if not previous_demand_history_amount_sum:
            return super(DemandHistory, self).save(force_insert=False, force_update=False, using=None,
                                                   update_fields=None)

        if self.amount > abs(previous_demand_history_amount_sum):
            raise WithdrawMoreThanDebt

        return super(DemandHistory, self).save(force_insert=False, force_update=False, using=None,
                                               update_fields=None)

    @classmethod
    def add_to_demand_for_new_transaction(cls, amount, credit_cwallet, credit_transaction):
        demand = Demand.create_demand_for_new_transaction(credit_cwallet, credit_transaction)
        return cls.objects.create(amount=amount, demand=demand)
