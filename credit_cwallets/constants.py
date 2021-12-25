from django.utils.translation import gettext_lazy as _
from model_utils import Choices

CREDIT_CWALLET_CHOICES = Choices(
    (0, 'inactive', _('inactive')),
    (1, 'active', _('active')),
    (2, 'banned', _('banned')),
)
