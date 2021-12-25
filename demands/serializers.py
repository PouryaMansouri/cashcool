from rest_framework import serializers

from credit_card.demands.models import Demand


class DemandListSerializer(serializers.ModelSerializer):
    # release_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Demand
        fields = ["id",
                  "credit_cwallet",
                  "release_datetime",
                  "credit_transaction",
                  "status",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]



class DemandRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ["id",
                  "credit_cwallet",
                  "release_datetime",
                  "credit_transaction",
                  "status",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]
        depth = 2
