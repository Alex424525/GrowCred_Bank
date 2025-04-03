from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AccountViewSet

app_name = 'accounts'

# REST Framework 라우터 설정
router = DefaultRouter()
router.register(r'api/accounts', AccountViewSet, basename='account')

urlpatterns = [
    path('personal-banking/', views.personal_banking, name='personal_banking'),
    path('create-account/', views.create_account, name='create_account'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('accounts/<int:account_id>/delete/', views.delete_account, name='delete_account'),
# accounts/urls.py 파일에 다음 URL 패턴을 추가하세요
    path('accounts/delete-selected/', views.delete_selected_accounts, name='delete_selected_accounts'),
    # REST API 엔드포인트
    path('', include(router.urls)),
]