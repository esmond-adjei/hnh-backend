from django.test import TestCase
from .models import HUser
from django.urls import reverse

class HUserManagementTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

    def test_01_user_creation(self):
        # Test creating a new user
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, 201)  # Expecting a successful user creation status code
        self.assertTrue(HUser.objects.filter(username='testuser').exists())  # HUser object should exist in the database

    def test_02_user_login(self):
        # Test user login
        response = self.client.post(reverse('login'), data=self.user_data)
        self.assertEqual(response.status_code, 200)  # Expecting a successful login status code
        self.assertTrue('token' in response.json())  # Expecting a token to be returned in the response
