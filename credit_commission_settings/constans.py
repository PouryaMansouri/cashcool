from django.utils.translation import gettext_lazy as _
from model_utils import Choices

COMMISSION_TYPE_CHOICES = Choices(
    (0, 'percentage', _("Percentage")),
    (1, "fixed_amount", _("Fixed Amount"))
)

BASE_ON_CHOICES = Choices(
    (0, "credit_tx_amount", _("credit Transaction Amount")),
    (1, "another_commission_setting_obj", _("Another Commission Setting Object"))
)
