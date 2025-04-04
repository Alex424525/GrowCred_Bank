from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-x*bw7&m6=k@%$#a=jbybpf-ajeid6(pdwzml!g)&lo8biuhk2k'


# DEBUG 설정 추가 - 개발 환경에서는 True로 설정
DEBUG = True

# ALLOWED_HOSTS 설정 추가
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '44.203.137.219']

AUTH_USER_MODEL = 'users.CustomUser'  # 사용자 모델 변경 (기본 User → CustomUser)

# SimpleJWT 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # 액세스 토큰 유효 시간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # 리프레시 토큰 유효 시간
    'ROTATE_REFRESH_TOKENS': True,                   # 리프레시 토큰 재발급 시 갱신
    'BLACKLIST_AFTER_ROTATION': True,                # 이전 토큰은 블랙리스트 처리

    'AUTH_HEADER_TYPES': ('Bearer',),                # Authorization 헤더 타입
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    'TOKEN_BLACKLIST_ENABLED': True,                 # 블랙리스트 기능 활성화 (로그아웃 시 필요)
}

INSTALLED_APPS = [
    # Django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # 직접 만든 앱
    'apps.users',

    # 입출금 앱
    'transactions',
    'accounts',


    # 외부 라이브러리
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "storages", # django-storages boto3 : static, media 같은 파일을 저장소와 연결해주는 라이브러리
]

# Static, Media URL 수정
STATIC_URL = f'https://{os.getenv("S3_STORAGE_BUCKET_NAME", "django-mini-project")}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{os.getenv("S3_STORAGE_BUCKET_NAME", "django-mini-project")}.s3.amazonaws.com/media/'


# STORAGES 작성
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_ACCESS_KEY", ""),
            "secret_key": os.getenv("S3_SECRET_ACCESS_KEY", ""),
            "bucket_name": os.getenv("S3_STORAGE_BUCKET_NAME", ""),
            "region_name": os.getenv("S3_REGION_NAME", ""),
            "location": "media",
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_ACCESS_KEY", ""),
            "secret_key": os.getenv("S3_SECRET_ACCESS_KEY", ""),
            "bucket_name": os.getenv("S3_STORAGE_BUCKET_NAME", ""),
            "region_name": os.getenv("S3_REGION_NAME", ""),
            "custom_domain": f'{os.getenv("S3_STORAGE_BUCKET_NAME", "")}.s3.amazonaws.com',
            "location": "static",
            "default_acl": "public-read",
        },
    },
}

# DB연결 정보
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "NAME": os.getenv("DB_NAME", "django"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 이 값은 각 환경(dev.py, prod.py)에서 오버라이드함

ROOT_URLCONF = 'config.urls'  # 기본값 추가


# Django REST Framework 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT 인증 기본 적용
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 모든 요청 인증 필요
    ),
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 템플릿 폴더 경로
        'APP_DIRS': True,  # 앱 폴더 내의 templates 디렉토리 자동 탐색
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# 데이터베이스 설정 추가
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


# 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = '/users/login/'

# 언어 및 시간 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 경로
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
