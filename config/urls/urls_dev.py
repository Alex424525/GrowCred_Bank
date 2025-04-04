"""
개발 환경 URL 설정
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from apps.users.views import home_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('apps.users.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path("logout/", LogoutView.as_view(), name="account_logout"),

    # JWT 토큰 발급 / 갱신
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
