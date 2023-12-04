from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from credit_management.models import Credit

class TestCredit(APITestCase):
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

    def test_build_credit(self):
        header = self.login_account()
        self.client.post('/credit/build/', data={
            "balance": "20",
        }, format='json', **header)
        credit = Credit.objects.first()
        self.assertEqual(credit.user, self.account1)
