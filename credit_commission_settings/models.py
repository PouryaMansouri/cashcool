from django.db import models

from credit_card.credit_commission_settings.constans import COMMISSION_TYPE_CHOICES
from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.credit_marketers.models import CreditMarketer
from cwallets.models import CWalletRegular


class CreditCommissionSetting(models.Model):
    credit_marketer = models.ForeignKey(CreditMarketer, on_delete=models.CASCADE)
    receiver = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE, related_name='commission_receiver')
    # TODO: commission only for add user for referral , add user and add club for cashcool
    club = models.ForeignKey(CreditCwallet, on_delete=models.CASCADE)

    type = models.IntegerField(choices=COMMISSION_TYPE_CHOICES, default=COMMISSION_TYPE_CHOICES.percentage)
    quantity = models.DecimalField(max_digits=9, decimal_places=3)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit_commission_setting"
        unique_together = ['credit_marketer', 'receiver', 'club']

    def __str__(self):
        return "{} | {} | {} | {}".format(self.credit_marketer, self.receiver, self.club, self.quantity)
