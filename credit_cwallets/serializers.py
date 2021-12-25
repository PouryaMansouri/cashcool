from rest_framework import serializers

from .models import CreditCwallet


class ListCreditCwalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCwallet
        fields = ["id",
                  "cwallet",
                  "current_cashtag",
                  "credit_amount",
                  "balance",
                  "credit_marketer",
                  "status",
                  "is_demand",
                  "demand_setting",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]
        depth = 2


class CreateCreditCwalletSerializer(serializers.ModelSerializer):
    # TODO: add all serialiers that need to create Credit Cwallet

    class Meta:
        model = CreditCwallet
        fields = ["id",
                  "cwallet",
                  "current_cashtag",
                  "credit_amount",
                  "balance",
                  "credit_marketer",
                  "status",
                  "is_demand",
                  "demand_setting",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]

    def create(self, validated_data):
        pass

    # TODO: add all serialiers that need to create Credit Cwallet
    # cwallet_data=validated_data.pop('cwallet')
    # cwallet_serializer = CreateCwalletSerializer(cwallet_data)
