"""
개발 환경 URL 설정
"""
from django.contrib import admin
from django.urls import path, include

from apps.users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('users/', include('apps.users.urls')),
]