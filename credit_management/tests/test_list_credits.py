from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from credit_management.models import Credit

class TestListCredit(APITestCase):
    def login_account(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": "SAliB",
            "password": "123Aa123"
        }, format='json')
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        return header
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/', data={
            "username": "SAliB",
            "password": "123Aa123",
        }, format='json')
        self.account1 = User.objects.get(username="SAliB")

    def test_list_credit(self):
        header = header = self.login_account()
        response = self.client.get('/credit/list/', **header)
        self.assertEqual(response.status_code, 200)
