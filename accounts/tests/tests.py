from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser1', 'password': 'testuser1'}
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        url = '/accounts/login/'
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_logout(self):
        url = '/accounts/login/'
        response = self.client.post(url, self.user_data, format='json')
        token = response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        print(header)
        new_response = self.client.post('/accounts/logout/', format='json', **header)
        print(new_response.status_code)
        self.assertEqual(new_response.status_code, status.HTTP_204_NO_CONTENT)

