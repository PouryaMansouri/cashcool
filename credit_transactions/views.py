from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from credit_card.credit_transactions.models import CreditTransaction
from credit_card.credit_transactions.serializers import CreditTransactionCreateSerializer, \
    CreditTransactionListSerializer


class CreditTransactionListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return CreditTransaction.objects.filter(sender__cwallet__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CreditTransactionListSerializer

        elif self.request.method == 'POST':
            return CreditTransactionCreateSerializer
