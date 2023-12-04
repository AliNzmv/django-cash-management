from django.test import TestCase, Client
from accounts.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class RegisterTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/accounts/register/', data={
            "username": "SAliB",
            "password": "123Aa123",
            "phone": "09383833833",
            "address": "Iran Tehran",
            "gender": "M",
            "age": "19",
            "first_name": "Seyed Ali",
            "last_name": "Babaei",
            "email": "SAliBSAliB@gmail.com"
        }, format='json')
        self.account1 = User.objects.get(username="SAliB")

    def test_register(self):
        self.assertTrue(self.account1 in User.objects.all())
