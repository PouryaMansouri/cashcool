from rest_framework import permissions

from credit_card.credit_marketers.models import CreditMarketer


class IsMarketer(permissions.BasePermission):

    def has_permission(self, request, view):
        marketer = CreditMarketer.objects.filter(marketer_cwallet__user=request.user)
        if marketer:
            return True
        return False


