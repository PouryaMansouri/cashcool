from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework import status


class DebtRepaymentBadDataException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("Debt Data Is Not Valid.")}


class BadDebtCreditTransactionObject(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("Debt Transaction Amount Can't be Positive.")}


class BadDebtRepaymentCreditTransactionObject(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("Debt Repayment Transaction Amount Can't be Negative.")}


class RepaymentMoreThanDebt(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("Debt Repayment Transaction Amount is more than debt.")}


class ThisDebtPenaltyCreateRepetitive(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("You want to create repetitive debt penalty ")}


class CalculateDebtPenaltyEverydayErrors(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'error': _("You want to create repetitive debt penalty ")}

    def __init__(self, errors: list, count_success, count_fails):
        self.errors = errors
        self.message = str({'errors': self.errors, 'count_success': count_success, 'count_fail': count_fails})
        self.default_detail = default_detail = {'error': _(self.message)}

    def __str__(self):
        return str(self.default_detail)
