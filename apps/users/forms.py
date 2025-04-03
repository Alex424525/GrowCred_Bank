# django의 폼 기능을 사용하기 위해 불러옴
from django import forms
# django 에서 기본 제공하는 회원기입 , 로그인 폼
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# 현재 폴더에 models.py 의 class : CustomUser 가져옴
from .models import CustomUser



# 회원가입 폼 클래스 정의 -> django 기본 UserCreationForm 을 상속
class SignupForm(UserCreationForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='생년월일'
    )

    # 폼 내부 설정 클라스 -> 어떤 모델 기반으로 만들지, 어떤 필드를 쓸지 정하는것
    class Meta:
        model = CustomUser      # 이 폼은 CustomUser 모델을 기반으로 작동
        fields = [
            'username',         # 사용자 id
            'email',            # 이메일 ( 마케팅 과 알림용 )
            'phone_number',     # 전화번호 ( 본인 인증용 )
            'full_name',        # 사용자 이름 ( 실명 )
            'birthdate',        # 생년월일
            'address'           # 주소
        ]
        labels = {
            'username': '아이디',
            'email': '이메일',
            'phone_number': '휴대폰 번호',
            'full_name': '이름',
            'birthdate': '생년월일',
            'address': '주소',
        }

# 로그인 폼: 사용자 인증용 폼
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'