from rest_framework import permissions

from credit_card.credit_cwallets.models import CreditCwallet


class IsOwnerCreditCwallet(permissions.BasePermission):

    def has_permission(self, request, view):
        owner = CreditCwallet.objects.filter(cwallet__user=request.user)
        if owner:
            return True
        return False
