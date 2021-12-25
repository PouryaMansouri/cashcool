from rest_framework import serializers

from base_everything.constants import LOWER_BASE_CASHTAG
from cwallets.models import CWalletRegular
from .models import ImportUserRequest
from ..credit_marketers.models import CreditMarketer


class ImportUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportUserRequest
        fields = ['excel_file']

    def create(self, validated_data):
        # should be admin
        validated_data['receiver'] = CWalletRegular.objects.filter(user__role=2, current_cashtag__cashtag=LOWER_BASE_CASHTAG)[0]
        validated_data['sender'] = CreditMarketer.objects.filter(marketer_cwallet__user=self.context['request'].user)[0]

        import_users_request_obj = ImportUserRequest.objects.create(**validated_data)

        return import_users_request_obj
