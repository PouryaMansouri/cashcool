from django.utils.translation import gettext_lazy as _
from model_utils import Choices

DEMADN_SETTING_TYPE_CHOICES = Choices(
    (0, "fixed_amount", _("Fixed Amount")),
    (1, "fixed_time", _("Fixed Time")),
    (2, "period_day", _("Period Day"))
)
