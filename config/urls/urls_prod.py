"""
배포 환경 URL 설정
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 프로덕션 환경에서는 Swagger 문서를 비활성화하거나 인증을 요구할 수 있음
]