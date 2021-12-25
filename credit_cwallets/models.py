from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from credit_card.credit_cwallets.constants import CREDIT_CWALLET_CHOICES
from credit_card.credit_marketers.models import CreditMarketer
from credit_card.demands_settings.models import DemandSetting
from cwallets.models import CWallet, Cashtags, CWalletRegular
from publics.exceptions import NotEnoughBalance
from .exceptions import CurrentCashtagAndCwalletAreNotCompatible


# currency is rial


class CreditCwallet(CWallet):
    cwallet = models.ForeignKey("cwallets.CWalletRegular", on_delete=models.CASCADE)

    current_cashtag = models.ForeignKey("cwallets.Cashtags", on_delete=models.CASCADE, null=True, blank=True)
    # TODO it's just a refrence for knowign what credit amount is belong to user. maybe it will be another good solution.
    credit_amount = models.DecimalField(max_digits=10, decimal_places=0,
                                        validators=[MaxValueValidator(1000000000), MinValueValidator(0)], )
    balance = models.DecimalField(max_digits=10, decimal_places=0,
                                  validators=[MaxValueValidator(1000000000), MinValueValidator(0)])
    credit_marketer = models.ForeignKey(CreditMarketer, on_delete=models.CASCADE)
    checkout_period_month = models.PositiveIntegerField()
    status = models.IntegerField(choices=CREDIT_CWALLET_CHOICES, default=CREDIT_CWALLET_CHOICES.active)

    is_demand = models.BooleanField(default=False)
    demand_setting = models.ForeignKey(DemandSetting, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit_cwallet"

    __original_credit_amount = None

    def __init__(self, *args, **kwargs):
        super(CreditCwallet, self).__init__(*args, **kwargs)
        self.__original_credit_amount = self.credit_amount

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # TODO credit amoutn just can edit with admin
        # TODO balance has to be less than credit amount
        # if self.credit_amount != self.__original_credit_amount:
        #     pass

        if self.current_cashtag:
            if not self.current_cashtag.cc_account.user == self.cwallet.user:
                raise CurrentCashtagAndCwalletAreNotCompatible

        if not self.is_demand:
            self.demand_setting = None

        return super(CreditCwallet, self).save(force_insert=False, force_update=False, using=None,
                                               update_fields=None)

    def __str__(self):
        return self.current_cashtag.cashtag if self.current_cashtag else self.cwallet.user.phone_number

    def reduce_credit_cwallet_balance(self, amount: Decimal):
        if self.balance - amount < 0:
            raise NotEnoughBalance
        self.balance = self.balance - amount
        self.save()

        return self.balance
    #
    # def increase_credit_cwallet_balance(self, amount: Decimal):
    #     self.balance = self.balance + amount
    #     self.save()
    #
    #     return self.balance
