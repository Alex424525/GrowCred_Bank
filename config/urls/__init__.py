"""
URL 패키지 초기화 파일
개발/배포 환경에 따라 적절한 URL 설정을 로드
"""
import os

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.prod':
    from .urls_prod import *
else:
    from .urls_dev import *