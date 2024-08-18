from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model 
from rest_framework import status
from account.models import User, FriendshipRequest

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

class FriendshipTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = get_user_model().objects.create_user(name='user1', password='password', email='user1@example.com')
        self.user2 = get_user_model().objects.create_user(name='user2', password='password', email='user2@example.com')

        self.friends_url = reverse('friends', kwargs={'pk': self.user1.pk})
        self.send_request_url = reverse('send_friendship_request', kwargs={'pk': self.user2.pk})
        self.handle_request_url = reverse('handle_request', kwargs={'pk': self.user2.pk, 'status': 'accepted'})
        
    # def test_get_friends(self):
    #     self.client.force_authenticate(user=self.user1)

    #     response = self.client.get(self.friends_url)

    #     # Debugging log
    #     print(f"Response status code: {response.status_code}")
    #     print(f"Response JSON: {response.json()}")

    #     self.assertEqual(response.status_code, 200)

    #     self.assertEqual(response.json()['user']['username'], self.user1.username)
    #     self.assertEqual(len(response.json()['friends']), 0)
    #     self.assertEqual(len(response.json()['requests']), 0)

    def test_send_friendship_request(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(self.send_request_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FriendshipRequest.objects.filter(created_by=self.user1, created_for=self.user2).count(), 1)
        self.assertEqual(response.json()['message'], 'Friendship request created')


    # def test_send_duplicate_friendship_request(self):
    #     # Authenticate as user1
    #     self.client.force_authenticate(user=self.user1)

    #     # Create a pre-existing request
    #     FriendshipRequest.objects.create(created_for=self.user2, created_by=self.user1)
        
    #     # Attempt to send a duplicate request
    #     response_duplicate = self.client.post(self.send_request_url)
        
    #     # Print for debugging
    #     print("Response status code:", response_duplicate.status_code)
    #     print("Response JSON:", response_duplicate.json())
    #     print("FriendshipRequest count:", FriendshipRequest.objects.filter(created_by=self.user1, created_for=self.user2).count())
        
    #     # Verify that the response indicates the request was already sent
    #     self.assertEqual(response_duplicate.status_code, 200)
    #     self.assertEqual(response_duplicate.json()['message'], 'request already sent')
        
    #     # Verify the number of requests to ensure correct behavior
    #     self.assertEqual(FriendshipRequest.objects.filter(created_by=self.user1, created_for=self.user2).count(), 1)

    def test_handle_request_accept(self):
        # Create a friendship request
        FriendshipRequest.objects.create(created_by=self.user2, created_for=self.user1)

        self.client.force_authenticate(user=self.user1)

        # Send POST request to handle the request
        response = self.client.post(self.handle_request_url)

        self.assertEqual(response.status_code, 200)

        # Verify the request status has been updated
        friendship_request = FriendshipRequest.objects.get(created_by=self.user2, created_for=self.user1)
        self.assertEqual(friendship_request.status, 'accepted')

        # Verify friends relationships
        self.assertTrue(self.user1.friends.filter(pk=self.user2.pk).exists())
        self.assertTrue(self.user2.friends.filter(pk=self.user1.pk).exists())

        # Verify friends count
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.friends_count, 1)
        self.assertEqual(self.user2.friends_count, 1)
        self.assertEqual(response.json()['message'], 'friendship request updated')