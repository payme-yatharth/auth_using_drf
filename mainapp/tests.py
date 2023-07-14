
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import status


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = AuthToken.objects.create(user=self.user)

    def test_register_api(self):
        url = '/api/register/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)

    def test_login_api(self):
        url = '/api/login/'
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


    from knox.models import AuthToken

    def test_change_password_view(self):
        url = '/api/change-password/'
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword'
        }
        token = AuthToken.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.token_key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_change_password_view_unauthorized(self):
        url = '/api/change-password/'
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from unittest.mock import patch
from .views import ChangePasswordView


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_change_password_invalid_request(self):
        url = '/api/change-password/'
        data = {
            'old_password': 'wrong_password',
            'new_password': 'newpassword'
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_valid_request(self):
        url = '/api/change-password/'
        data = {
            'old_password': 'password@123',
            'new_password': 'password@1234'
        }
        self.client.login(username='testusercheck', password='password@123')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('requests.put')
    def test_change_password_external_api_request(self, mock_put):
        url = '/api/change-password/'
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword'
        }
        self.client.login(username='testuser', password='testpassword')
        mock_put.return_value.json.return_value = {'response_data': 'mocked_data'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK
                         )



