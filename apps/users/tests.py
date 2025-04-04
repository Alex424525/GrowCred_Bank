from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status  # ← 상수 사용을 위해 유지

class UserTestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('users:logout')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@naver.com',
            'phone_number': '01033993084',
            'full_name': '김정대',
            'birthdate': '1945-06-05',
            'address': '경기도 화성시',
            'password': 'test1234',
            'password2': 'test1234',
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        # 회원가입 먼저 수행
        self.client.post(self.signup_url, self.user_data)

        # 로그인 요청
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout(self):
        # 회원가입 및 로그인
        self.client.post(self.signup_url, self.user_data)

        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # 로그아웃 요청
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
