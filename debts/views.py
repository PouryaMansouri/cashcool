from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from credit_card.debts.exceptions import DebtRepaymentBadDataException
from credit_card.debts.models import Debt, DebtRepayment, DebtPenalty
from credit_card.debts.permissions import IsOwnerCreditCwallet
from credit_card.debts.serializers import DebtRepaymentSerializer, \
    DebtListSerializer, DebtRetrieveSerializer, DebtPenaltyListSerializer, DebtPenaltyRetrieveSerializer


class DebtListView(ListAPIView):
    serializer_class = DebtListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Debt.objects.filter(credit_cwallet__cwallet__user=self.request.user)


class DebtPenaltyListView(ListAPIView):
    serializer_class = DebtPenaltyListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return DebtPenalty.objects.filter(debt__credit_cwallet__cwallet__user=self.request.user)


class DebtPenaltyRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DebtPenaltyRetrieveSerializer

    def get_queryset(self):
        return DebtPenalty.objects.filter(debt__credit_cwallet__cwallet__user=self.request.user, id=self.kwargs["pk"])


class DebtRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DebtRetrieveSerializer

    def get_queryset(self):
        return Debt.objects.filter(credit_cwallet__cwallet__user=self.request.user, id=self.kwargs["pk"])


class DebtRepaymentView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerCreditCwallet]

    def post(self, request, format=None):
        serializer = DebtRepaymentSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            DebtRepayment.do_repayment(credit_cwallet=validated_data['credit_cwallet'],
                                       cwallet=validated_data['cwallet'], amount=validated_data['amount'],
                                       context=request['context'], request=request)

        raise DebtRepaymentBadDataException
