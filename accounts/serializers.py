from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(read_only=True)

    class Meta:
        model = Account  # models가 아닌 model로 수정
        fields = [
            'id',  # id 필드 추가
            'user',
            'account_number',
            'bank_name',
            'account_name',  # account_name 필드 추가
            'balance',
            'password',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            "id",
            "account_number",
            "balance",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "password": {"write_only": True},  # 응답에 포함되지 않음
        }