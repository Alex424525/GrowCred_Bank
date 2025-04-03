import random
from django.db import models
from django.conf import settings


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100, default="저신용 은행")
    account_name = models.CharField(max_length=100, default="일반계좌")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    password = models.CharField(max_length=4)  # 4자리 비밀번호
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}의 {self.bank_name} 계좌 ({self.account_number})"

    @classmethod
    def generate_account_number(cls):
        """랜덤한 계좌번호 생성 (123-456-789012)"""
        while True:
            # 계좌번호 형식: XXX-XXX-XXXXXX
            first = str(random.randint(100, 999))
            second = str(random.randint(100, 999))
            third = str(random.randint(100000, 999999))
            account_number = f"{first}-{second}-{third}"

            # 이미 존재하는 계좌번호인지 확인
            if not cls.objects.filter(account_number=account_number).exists():
                return account_number


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', '입금'),
        ('WITHDRAW', '출금'),
        ('TRANSFER', '이체'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.get_transaction_type_display()} {self.amount} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
