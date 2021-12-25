from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from credit_card.demands.models import Demand
from credit_card.demands.serializers import DemandListSerializer, DemandRetrieveSerializer


class DemandListView(ListCreateAPIView):
    serializer_class = DemandListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Demand.objects.filter(credit_cwallet__cwallet__user=self.request.user)


class DemandRetrieveView(RetrieveUpdateAPIView):
    serializer_class = DemandRetrieveSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Demand.objects.filter(credit_cwallet__cwallet__user=self.request.user, id=self.kwargs["pk"])
