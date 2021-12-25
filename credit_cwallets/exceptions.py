from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework import status

HTTP_498_REVOKED = 498
HTTP_419_DID_NOT_SEND = 419


# ---------Credit Cwallet Exceprions-----------#


class CurrentCashtagAndCwalletAreNotCompatible(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Current cashtag and cwallet are not compatible")}
