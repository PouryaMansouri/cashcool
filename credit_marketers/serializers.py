##just super user can create marketer organization pair
from rest_framework import serializers

from credit_card.credit_marketers.models import CreditMarketer


class CreditMarketerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditMarketer
        fields = ["id",
                  "marketer_cwallet",
                  "organization",
                  "contract_img",
                  "bank_guarantee",
                  "financing_tracking_code",
                  "credit_amount",
                  "transaction_amount_remain",
                  "created_at",
                  "updated_at",
                  ]
        read_only_fields = ["id",
                            "created_at",
                            "updated_at", ]

        depth = 2

