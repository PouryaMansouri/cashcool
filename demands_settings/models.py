from django.db import models

from credit_card.demands_settings.constants import DEMADN_SETTING_TYPE_CHOICES
from .exceptions import BadWithdrawTypeAndValueSetting


class DemandSetting(models.Model):
    type = models.IntegerField(choices=DEMADN_SETTING_TYPE_CHOICES)
    value = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.type == DEMADN_SETTING_TYPE_CHOICES.fixed_amount:
            if self.value <= 0:
                raise BadWithdrawTypeAndValueSetting

        if self.type == DEMADN_SETTING_TYPE_CHOICES.fixed_time:
            if not 1 <= self.value <= 28:
                raise BadWithdrawTypeAndValueSetting

        if self.type == DEMADN_SETTING_TYPE_CHOICES.period_day:
            if not 1 <= self.value <= 365:
                raise BadWithdrawTypeAndValueSetting

        return super(DemandSetting, self).save(force_insert=False, force_update=False, using=None,
                                               update_fields=None)

    def __str__(self):
        return "type: {} --  value: {}".format(self.type, self.value)
