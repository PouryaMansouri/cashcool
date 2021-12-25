from rest_framework import serializers

from credit_card.credit_transactions.models import CreditTransaction
from .exceptions import NotCompatibleMarketerOrganization, SenderIsBanned, ClubIsBanned, \
    RepetitiveCreditTransaction, InvalidCreditTransactionAmount


class CreditTransactionCreateSerializer(serializers.ModelSerializer):
    send_signal = serializers.BooleanField(required=False, default=True)
    send_debt = serializers.BooleanField(required=False, default=True)
    pay_from_demand = serializers.BooleanField(required=False, default=False)
    commission_transaction = serializers.BooleanField(required=False, default=False)
    commission_transaction_parent = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = CreditTransaction
        fields = [
            "sender",
            "receiver",
            "amount",
            "commission_transaction",
            "commission_transaction_parent",
            "send_signal",
            "send_debt",
            "pay_from_demand"
        ]

    # def validate(self, attrs):
    #     # check repatitive tx:
    #
    #     sender = CreditTransaction.objects.filter(
    #         credit_cwallet_sender__credit_cwallet__cwallet__user=self.context["request"].user)
    #     if not sender:
    #         raise ValidationError(detail=_("Sender Does not exists."), code=404)

    def create(self, validated_data):
        try:
            send_signal = validated_data.pop('send_signal')
            send_debt = validated_data.pop('send_debt')
            pay_from_demand = validated_data.pop('pay_from_demand')
            tx_instance = super(CreditTransactionCreateSerializer, self).create(validated_data)
            tx_instance.do_transaction(send_signal=send_signal, send_debt=send_debt, pay_from_demand=pay_from_demand)
            return tx_instance

        except NotCompatibleMarketerOrganization:
            raise NotCompatibleMarketerOrganization

        except SenderIsBanned:
            raise SenderIsBanned

        except ClubIsBanned:
            raise ClubIsBanned

        except RepetitiveCreditTransaction:
            raise RepetitiveCreditTransaction

        except InvalidCreditTransactionAmount:
            raise InvalidCreditTransactionAmount


class CreditTransactionListSerializer(serializers.ModelSerializer):
    send_signal = serializers.BooleanField(required=False, default=True)
    send_debt = serializers.BooleanField(required=False, default=True)
    pay_from_demand = serializers.BooleanField(required=False, default=False)
    commission_transaction = serializers.BooleanField(required=False, default=False)
    commission_transaction_parent = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = CreditTransaction
        fields = [
            "sender",
            "receiver",
            "amount",
            "commission_transaction",
            "commission_transaction_parent",
            "send_signal",
            "send_debt",
            "pay_from_demand"
        ]
