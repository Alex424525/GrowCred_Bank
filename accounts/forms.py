from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    """계좌 생성 폼"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'maxlength': 4, 'pattern': '[0-9]{4}'}),
        max_length=4,
        help_text='4자리 숫자로 입력해주세요.'
    )

    class Meta:
        model = Account
        fields = ['bank_name', 'account_name', 'password']
        widgets = {
            'bank_name': forms.Select(choices=[
                ('저신용 은행', '저신용 은행'),
                ('국민 은행', '국민 은행'),
                ('신한 은행', '신한 은행'),
                ('우리 은행', '우리 은행'),
            ]),
            'account_name': forms.TextInput(attrs={'placeholder': '계좌 별칭'}),
        }

