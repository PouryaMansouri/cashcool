from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from credit_card.credit_marketers.models import CreditMarketer
from credit_card.credit_marketers.permissions import IsMarketer
from credit_card.credit_marketers.serializers import CreditMarketerSerializer


class CreditMarketerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsMarketer]
    serializer_class = CreditMarketerSerializer

    def get_queryset(self):
        return CreditMarketer.objects.filter(marketer_cwallet__user=self.request.user)


class CreditMarketerRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsMarketer]
    serializer_class = CreditMarketerSerializer

    def get_queryset(self):
        return CreditMarketer.objects.filter(marketer_cwallet__user=self.request.user)
