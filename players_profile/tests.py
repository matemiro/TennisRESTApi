from rest_framework.test import APITestCase
from authentication.models import User
from .models import Profile


class TestAuthentication(APITestCase):

    def setUp(self):

        self.username = 'testing_user'
        self.user_email = 'email@for.tests'
        self.password = 'dummypassword123'
        self.user = User.objects.create_user(username=self.username, email=self.user_email, password=self.password)

    def test_create_user(self):

        url = '/auth/signup/'
        data = {
            'username': 'dummyuser',
            'email': 'new@testing.email',
            'password': 'somenewpassword123'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        created_user = User.objects.filter(username='dummyuser')[0]

        self.assertTrue(created_user)
        self.assertEqual(created_user.email, 'new@testing.email')

        created_user_profile = Profile.objects.filter(user=created_user)

        self.assertTrue(created_user_profile)

    def test_jwt(self):

        url_to_create = '/auth/jwt/create/'
        url_to_verify = '/auth/jwt/verify/'
        data = {
            'email': self.user_email,
            'password': self.password
        }

        response = self.client.post(url_to_create, data=data)
        self.assertEqual(response.status_code, 200)

        result = response.json()
        self.assertIsInstance(result, dict)

        data = {
            'token': result.get('access')
        }
        response = self.client.post(url_to_verify, data=data)
        self.assertEqual(response.status_code, 200)

    def test_create_user_with_existing_email(self):
        url = '/auth/signup/'
        data = {
            'username': 'dummyuser',
            'email': self.user_email,
            'password': 'somenewpassword123'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_existing_username(self):
        url = '/auth/signup/'
        data = {
            'username': self.username,
            'email': 'some@new.email',
            'password': 'somenewpassword123'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
