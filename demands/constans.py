from django.utils.translation import gettext_lazy as _
from model_utils import Choices

DEMAND_STATUS = Choices(
    (0, "pending", _("Pending")),
    (1, "done", _("Done")),
    (2, "cancel", _("Cancel")),
    (3, "rejected", _("Rejected")),
)


DEMANDS_HISTORIES_STATUS = Choices(
    (0, "pay_to_club", _("Pay To Club")),
    (1, "withdraw", _("Withdraw")),
    (2, "shopping", _("Shopping")),
    (3,"pay_for_commission",_("Pay for Commission"))
)


