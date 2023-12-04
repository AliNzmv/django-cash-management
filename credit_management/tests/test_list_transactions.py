from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from credit_management.models import Credit

class TestReportTransaction(APITestCase):
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
        Credit.objects.create(user_id=2, balance=2000)


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

    def test_transaction_log_not_authenticated(self):
        self.build_credit()
        response = self.client.get('/credit/transactionreport/m/1/')
        self.assertEqual(response.status_code, 401)

    def test_transaction_log_not_owned(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.get('/credit/transactionreport/m/2/', **header)
        self.assertEqual(response.status_code, 400)

    def test_transaction_log_not_exist(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.get('/credit/transactionreport/m/4/', **header)
        self.assertEqual(response.status_code, 404)

    def test_transaction_log_invalid_choice(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.get('/credit/transactionreport/z/1/', **header)
        self.assertEqual(response.status_code, 404)

    def test_transaction_log(self):
        header = self.login_account()
        self.build_credit()
        response = self.client.get('/credit/transactionreport/m/1/', **header)
        self.assertEqual(response.status_code, 201)


