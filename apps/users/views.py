# django 에서 기본적으로 제공하는 기능들 불러오기
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect   # 페이지 보여주기 ( render ) 이동시키기 ( redirect )
from django.contrib import messages         # 회원가입 성공 과 실패 메시지

from rest_framework_simplejwt.tokens import RefreshToken

# 현제 폴더 애서 forms.py 에 class : SignupForm , LoginForm 가져옴
from .forms import SignupForm ,LoginForm
# django 에서 호그인 기능 가져오기
from django.contrib.auth import authenticate , login , logout






# 홈 뷰
def home_view(request):
    return render(request, 'users/home.html')



# 회원가입 뷰
def signup_view(request):
    # 사용자가 POST 방식으로 회원가입 폼 제출했을 때
    if request.method == 'POST':
        form = SignupForm(request.POST)  # 사용자가 입력한 데이터로 폼 생성

        if form.is_valid():     # 폼 검증 ( 모든 값이 맞는지 확인 )
            form.save()     # 사용자 정보를 DB에 저장
            messages.success(request, '축하합니다 로그인하면 당신의 새로운 인생을 도와드리겠습니다.')
            return redirect('users:login')      # 로그인 화면으로 이동
        else:
            messages.error(request, '입력한 정보가 올바르지 않습니다')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    # 맞지 않으면 다시 폼 보여주기 ( 입력갑을 유지 한체로 )
    return render(request, 'users/signup.html',context)

# 로그인 로그아웃 뷰
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)    # 사용자 입력 데이터? 값? 가져오기

        if form.is_valid():
            user = form.get_user()  # 로그인할 사용자 객체 가져오기
            login(request, user) # 로그인 처리
            return redirect('home')  # 홈으로 이동
        else:
            messages.error(request, '아이디 또는 비밀번호가 틀렸습니다.')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'users/login.html',context)

def logout_view(request):
    logout(request)     # 사용자 세션 삭제

    # 블랙리스트 처리
    refresh_token = request.COOKIES.get('refresh_token') # 쿠키에서 refresh 토큰 가져옴
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   # 블랙리스트 등록
        except Exception as e:
            print('블랙리스트 처리 오류',e)

    messages.success(request, '성곡적으로 로그아웃 되었습니다.')
    return redirect('home')



# 로그인 사용자만 접근 가능한 페이지
@login_required
def transfer_view(request):  # 계좌 이체
    return render(request, 'users/transfer.html')

@login_required
def transfer_view(request): # 계좌이체 -> 입금 출금 기능
    return render(request, 'users/transfer.html')

@login_required
def deposit_view(request):
    return render(request, 'users/dummy.html')  # 임시

@login_required
def withdraw_view(request):
    return render(request, 'users/dummy.html')  # 임시

@login_required
def transactions_view(request): # 거래 내역
    return render(request, 'users/transactions_view.html')

@login_required
def savings_view(request): # 저축
    return render(request, 'users/savings.html')

@login_required
def credit_cards_view(request): # 신용카드
    return render(request, 'users/credit_cred.html')

@login_required
def products_view(request):  # 금융상품
    return render(request, 'users/products.html')

@login_required
def consumer_protection_view(request): # 소비자보호
    return render(request, 'users/consumer.html')

@login_required
def research_view(request): # 디지털금융연구소
    return render(request, 'users/products.html')

@login_required
def account_inquiry_view(request): # 계좌 조회
    return render(request, 'users/account_inquiry.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account  # accounts 앱의 Account 모델 import


@login_required
def account_inquiry_view(request):
    """
    로그인한 사용자의 계좌 목록을 조회하는 뷰
    """
    # 현재 로그인한 사용자의 활성화된 계좌만 조회
    accounts = Account.objects.filter(user=request.user, is_active=True)

    context = {
        'accounts': accounts,
    }

    return render(request, 'users/account_inquiry.html', context)