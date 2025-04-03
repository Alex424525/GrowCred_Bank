from django import forms

from transactions.models import DepositModel, WithdrawalModel


# 입금 폼
class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositModel
        fields = ('amount', 'description','account')

        # TODO : 계좌랑 같은 사용자의 계좌만 보여주기

# 출금 폼
class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalModel
        fields = ('amount', 'description', 'account')

        # TODO : 계좌랑 같은 사용자의 계좌만 보여주기