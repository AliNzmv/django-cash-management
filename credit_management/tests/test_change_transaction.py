from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from credit_management.models import Credit, Transaction


class TestChangeTransaction(APITestCase):
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

    def build_transaction(self):
        self.build_credit()
        transaction1 = Transaction()
        transaction1.save()
        transaction1.credits.add(Credit.objects.get(id=1))
        transaction1.credits.add(Credit.objects.get(id=2))
        transaction1.money = 1000
        transaction1.category = 'g'
        transaction1.init_credit = 1
        transaction1.save()
        transaction2 = Transaction()
        transaction2.save()
        transaction2.credits.add(Credit.objects.get(id=2))
        transaction2.credits.add(Credit.objects.get(id=1))
        transaction2.money = 1000
        transaction2.category = 'g'
        transaction2.init_credit = 2
        transaction2.save()


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

    def test_update_transaction_not_exist(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.put('/credit/changetransaction/5/', data={
            "category": 'u',
        }, format='json', **header, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_transaction_not_owned(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.put('/credit/changetransaction/2/', data={
            "category": 'u',
        }, format='json', **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_transaction_invalid_choice(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.put('/credit/changetransaction/1/', data={
            "category": 'a',
        }, format='json', **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_transaction_not_authenticated(self):
        self.build_transaction()
        response = self.client.put('/credit/changetransaction/2/', data={
            "category": 'u',
        }, format='json', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_transaction_correct(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.put('/credit/changetransaction/1/', data={
            "category": "u"
        }, format='json', **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.get(id=1).category, 'u')

    def test_delete_transaction_not_exist(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.delete('/credit/changetransaction/5/', **header)
        self.assertEqual(response.status_code, 404)

    def test_delete_transaction_not_owned(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.delete('/credit/changetransaction/2/', **header)
        self.assertEqual(response.status_code, 400)

    def test_delete_transaction_not_owned(self):
        header = self.login_account()
        self.build_transaction()
        response = self.client.delete('/credit/changetransaction/1/', **header)
        self.assertEqual(response.status_code, 201)
