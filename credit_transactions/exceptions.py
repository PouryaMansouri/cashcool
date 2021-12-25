from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework import status

HTTP_498_REVOKED = 498
HTTP_419_DID_NOT_SEND = 419


# ----------Credit Cwallet Exceptions-----------#
# -----------Credit transactions Exceptions ---------#
class NotCompatibleMarketerOrganization(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Not Compatible Marketer Organization.")}


class BadReceiverInTransaction(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Receiver should be club.")}


class SenderIsBanned(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Sender Is Banned.")}


class ClubIsBanned(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Club Is Banned.")}


class TransactionWithBadCommissionData(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Data for Commission is not valid.")}


class RepetitiveCreditTransaction(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Repetitive Transaction Detected.")}


class InvalidCreditTransactionAmount(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("Transaction amount should be more than 1000.")}


class NotEnoughBalance(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'message': _("not enough balance.")}
