from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import HUser


class UserManagementTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone_number': '1234567890',
        }

    def test_user_registration(self):
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

        # Check if the user was created in the database
        user_id = response.data['user_id']
        self.assertTrue(HUser.objects.filter(id=user_id).exists())

    def test_user_login(self):
        # Create a test user for login
        user = HUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            phone_number='1234567890',
        )

        login_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_invalid_user_login(self):
        login_data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword',
        }

        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         'Invalid username or password')
