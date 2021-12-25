from rest_framework import serializers

from credit_card.debts.models import Debt, DebtPenalty


class DebtPenaltyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtPenalty
        fields = ["id",
                  "debt",
                  "penalty_amount",
                  "status",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]
        # depth = 1


class DebtPenaltyRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtPenalty
        fields = ["id",
                  "debt",
                  "penalty_amount",
                  "status",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]
        # depth = 1


class DebtListSerializer(serializers.ModelSerializer):
    penalty = serializers.SerializerMethodField()

    def get_penalty(self, object):
        penalty_obj = DebtPenalty.objects.filter(debt=object)
        validate_data = DebtPenaltyListSerializer(penalty_obj, many=True)
        return validate_data.data

    # def to_representation(self, instance):
    #     serializers_date = super(DebtListSerializer, self).to_representation(instance)
    #     serializers_date["penalty"] = DebtPenaltyListSerializer()
    #     return serializers_date

    class Meta:
        model = Debt
        fields = ["id",
                  "credit_cwallet",
                  "credit_transaction",
                  "status",
                  "repayment_date_time",
                  "penalty",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]


class DebtRetrieveSerializer(serializers.ModelSerializer):
    penalty = serializers.SerializerMethodField()

    def get_penalty(self, object):
        penalty_obj = DebtPenalty.objects.filter(debt=object)
        validate_data = DebtPenaltyListSerializer(penalty_obj, many=True)
        return validate_data.data

    class Meta:
        model = Debt
        fields = ["id",
                  "credit_cwallet",
                  "credit_transaction",
                  "status",
                  "repayment_date_time",
                  'penalty',
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]


class DebtRepaymentSerializer(serializers.Serializer):
    cwallet = serializers.SerializerMethodField()

    def get_cwallet(self, obj: str):
        if obj.isdigit():
            cwallet = serializers.IntegerField(required=True)
            return cwallet
        cwallet = serializers.CharField(required=True)
        return cwallet

    credit_cwallet = serializers.SerializerMethodField()

    def get_credit_cwallet(self, obj: str):
        if obj.isdigit():
            credit_cwallet = serializers.IntegerField(required=True)
            return credit_cwallet
        credit_cwallet = serializers.CharField(required=True)
        return credit_cwallet

    amount = serializers.DecimalField(required=True, max_digits=9, decimal_places=0)
