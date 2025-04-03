"""
개발 환경 URL 설정
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from apps.users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('apps.users.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path("logout/", LogoutView.as_view(), name="account_logout"),
]