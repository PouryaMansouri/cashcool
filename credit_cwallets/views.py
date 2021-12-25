# Create your views here.
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.credit_cwallets.serializers import ListCreditCwalletSerializer, CreateCreditCwalletSerializer


class CreditCwalletListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return CreditCwallet.objects.filter(cwallet__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCreditCwalletSerializer

        elif self.request.method == 'POST':
            return CreateCreditCwalletSerializer
