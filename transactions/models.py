from django.db import models

from accounts.models import Account
from config import settings
from utils.time_models import DepositTimestampModel, WithdrawTimestampModel


# 사용자의 은행 계좌 정보를 받아온다. : Account ID 지금은 일단 제외
# 계좌 정보를 받아와서 해당 계좌 정보와 입출금 기능을 사용하는 사람이 일치 하면
# 계좌에서 입출금이 가능 하도록 구현




# 입금 모델
class DepositModel(DepositTimestampModel):
    # 거래 고유 ID
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='deposits', null=False, blank=False)
    amount = models.DecimalField('입금', max_digits=15, decimal_places=2)  # 입출금 금액
    description = models.TextField(blank=True, null=True)  # 거래 설명 (옵션)


# 출금 모델
class WithdrawalModel(WithdrawTimestampModel):
    # 거래 고유 ID
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField('출금', max_digits=15, decimal_places=2)  # 입출금 금액
    description = models.TextField(blank=True, null=True)  # 거래 설명 (옵션)
