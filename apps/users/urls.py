from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    # 회원
    path('signup/', views.signup_view, name='signup'),     # 회원가입 URL
    path('login/', views.login_view, name='login'),         # 로그인 URL
    path('logout/', views.logout_view, name='logout'),      # 로그아웃 URL
    path('profile/', views.profile_view, name='profile'),   # 정보 좋회
    path('profile/update/', views.profile_update_view, name='profile_update'),      # 정보 수정
    path('profile/delete/', views.delete_view, name='profile_delete'),      # 회원 탈퇴

    # 겨좌 이체 -> 입금,출금
    path('transfer/', views.transfer_view, name='transfer'),  # 계좌 이체
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),

    # 다른 서비스
    path('transactions/', views.transactions_view, name='transactions'),  # 거래 내역
    path('savings/', views.savings_view, name='savings'),  # 저축
    path('credit-cards/', views.credit_cards_view, name='credit_cards'),  # 신용카드
    path('products/', views.products_view, name='products'),  # 금융상품
    path('consumer/', views.consumer_protection_view, name='consumer'),  # 소비자 보호
    path('research/', views.research_view, name='research'),  # 디지털금융연구소
    path('accounts-inquiry/', views.account_inquiry_view, name='accounts_inquiry'),  # 계좌 조회
    path('home/', views.home_view, name='home'),    # 메인으로 가기
]