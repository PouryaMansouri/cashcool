from django.utils.translation import gettext_lazy as _
from model_utils import Choices

TRANSACTION_STATUS_CHOICES = Choices(
    (0, 'pending', _('Pending')),
    (1, 'success', _('Success')),
    (2, 'cancel', _('Cancel')),
    (3, 'reject', _('Reject'))
)
