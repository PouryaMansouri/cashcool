import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from credit_card.credit_marketers.exceptions import BadNameInput, BadNicknameInput
from credit_card.credit_marketers.validators import validate_organization_nikename, validate_organization_name


class Organization(models.Model):
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not validate_organization_name:
            raise BadNameInput

        if not validate_organization_nikename(self.nickname):
            raise BadNicknameInput

        return super(Organization, self).save(force_insert=False, force_update=False, using=None,
                                              update_fields=None)


# TODO: reduce credit after each transaction
# TODO: check transaction_amount_remain before transaction
# TODO: verify with sms
class CreditMarketer(models.Model):
    def contract_upload_path(instance, filename):
        return os.path.join(settings.MEDIA_ROOT, 'credit_card', instance.marketer_cwallet.current_cashtag.cashtag,
                            'contract', filename)

    def bank_guarantee_path(instance, filename):
        return os.path.join(settings.MEDIA_ROOT, 'credit_card', instance.marketer_cwallet.current_cashtag.cashtag,
                            'bank_guarantee', filename)

    marketer_cwallet = models.ForeignKey("cwallets.CWalletRegular", on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    contract_img = models.ImageField(upload_to=contract_upload_path, null=True, blank=True)
    bank_guarantee = models.ImageField(upload_to=bank_guarantee_path, null=True, blank=True)

    financing_tracking_code = models.CharField(max_length=20, null=True, blank=True)
    # TODO if this amount related to a credit deposit or not

    credit_amount = models.DecimalField(max_digits=13, decimal_places=0, default=0)

    transaction_amount_remain = models.DecimalField(max_digits=13, decimal_places=0, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "credit_marketer"

    def __str__(self):
        marketer_first_name = self.marketer_cwallet.user.first_name if self.marketer_cwallet.user.first_name else None
        marketer_last_name = self.marketer_cwallet.user.last_name if self.marketer_cwallet.user.last_name else None
        marketer_phone_number = self.marketer_cwallet.user.phone_number
        introducer_string = ""
        for i in [marketer_first_name, marketer_last_name, marketer_phone_number]:
            if i:
                introducer_string = introducer_string + " | " + i

        introducer_string = introducer_string + " | " + self.organization.name
        return introducer_string
