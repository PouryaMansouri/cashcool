from django.utils.translation import gettext_lazy as _
from model_utils import Choices

IMPORT_USER_REQUEST_CHOICES = Choices((0, 'pending', _('Pending')),
                                      (1, 'processed', _('Processed')),
                                      (2, 'accepted', _('Accepted')),
                                      (3, 'partial_accepted', _('PartialAccepted')),
                                      (4, 'rejected', _('Rejected'))
                                      )
CORRECT_IMPORT_USER_REQUEST_EXCEL_HEADER = ['phone_number', 'first_name', 'last_name', 'credit', 'refund_period',
                                            'refund_amount', 'credit_month_limit']
