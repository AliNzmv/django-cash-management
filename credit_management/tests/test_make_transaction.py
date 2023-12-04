from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from credit_management.models import Credit

class TestMakeTransaction(APITestCase):
    def login_account(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": "user1",
            "password": "123Aa123"
        }, format='json')
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        return header

    def build_credit(self):
        Credit.objects.create(user_id=1, balance=2000)
        Credit.objects.create(user_id=2, balance=0)

    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/', data={
            "username": "user1",
            "password": "123Aa123",
        }, format='json')
        self.client.post('/accounts/register/', data={
            "username": "user2",
            "password": "123Aa123",
        }, format='json')

    def test_make_transaction_not_authenticated(self):
        self.build_credit()
        response = self.client.post('/credit/transaction/', data={
            "from_credit": 2,
            "to_credit": 1,
            "money": 1000,
            "category": "g"
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_make_transaction_not_owned_credit(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.post('/credit/transaction/', data={
            "from_credit": 2,
            "to_credit": 1,
            "money": 1000,
            "category": "g"
        }, format='json', **header)
        self.assertEqual(response.status_code, 400)

    def test_make_transaction_not_exist_id(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.post('/credit/transaction/', data={
            "from_credit": 4,
            "to_credit": 1,
            "money": 1000,
            "category": "g"
        }, format='json', **header)
        self.assertEqual(response.status_code, 404)
    def test_make_transaction_invalid_category(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.post('/credit/transaction/', data={
            "from_credit": 4,
            "to_credit": 1,
            "money": 1000,
            "category": "g"
        }, format='json', **header)
        self.assertEqual(response.status_code, 404)

    def test_make_transaction_correct(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.post('/credit/transaction/', data={
            "from_credit": 1,
            "to_credit": 2,
            "money": 1000,
            "category": "g"
        }, format='json', **header)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Credit.objects.get(id=1).balance, 1000)
        self.assertEqual(Credit.objects.get(id=2).balance, 1000)


