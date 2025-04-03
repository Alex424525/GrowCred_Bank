from django.db import models

class DepositTimestampModel(models.Model):
    # 입금 시간
    deposit_at = models.DateTimeField('입금 시간', auto_now_add=True)

    # abstract(추상 모델) = True를 설정한 모델은 직접 테이블로 생성되지 않음
    class Meta:
        abstract = True
        ordering = ['-deposit_at']

class WithdrawTimestampModel(models.Model):
    # 출금 시간
    withdrawal_at = models.DateTimeField('출금 시간', auto_now_add=True)

    # abstract(추상 모델) = True를 설정한 모델은 직접 테이블로 생성되지 않음
    class Meta:
        abstract = True
        ordering = ['-withdrawal_at']