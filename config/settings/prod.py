from .base import *

DEBUG = False  # 운영 환경에서는 디버깅 정보 표시 금지

ALLOWED_HOSTS = ["44.203.137.219"] # EC2 퍼블릭 IP

ROOT_URLCONF = 'config.urls.urls_prod'  # 운영 전용 URL 설정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bank',
        'USER': 'dev_user',
        'PASSWORD': 'securepassword',
        'HOST': 'db',  # Docker 컨테이너 내 DB 서비스 이름
        'PORT': '5432',
    }
}