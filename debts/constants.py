from django.utils.translation import gettext_lazy as _
from model_utils import Choices

DEBT_STATUS_CHOICES = Choices(
    (0, "not_payed", _("Not Payed")),
    (1, "payed", _("Payed"))
)

DEBT_PENALTY_STATUS_CHOICES = Choices(
    (0, "not_payed", _("Not Payed")),
    (1, "payed", _("Payed"))
)

BANK_PENALTY_RATE = 0.06
