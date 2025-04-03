from .base import *

DEBUG = True  # 개발 중에는 디버깅 정보 표시

ALLOWED_HOSTS = ['*']  # 개발 환경에서는 모든 호스트 허용

ROOT_URLCONF = 'config.urls.urls_dev'  # 개발 전용 URL 설정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bank',
        'USER': 'dev_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '54322',
    }
}