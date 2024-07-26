from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import User

class AccountTests(APITestCase):
    def test_signup_success(self):
        url = reverse('signup')
        data = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_signup_password_mismatch(self):
        url = reverse('signup')
        data = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'password1': 'strongpassword123',
            'password2': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'error')
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())

    def test_me_authenticated(self):
        user = User.objects.create_user(email='testuser@example.com', name='Test User', password='strongpassword123')
        self.client.force_authenticate(user=user)
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], str(user.id))
        self.assertEqual(response.json()['name'], user.name)
        self.assertEqual(response.json()['email'], user.email)

    def test_me_unauthenticated(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

