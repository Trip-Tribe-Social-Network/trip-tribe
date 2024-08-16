from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from post.models import Post

User = get_user_model()

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.friend = User.objects.create_user(name='friend', email='friend@example.com', password='password')
        self.user.friends.add(self.friend)
        self.post = Post.objects.create(body='Test Post', created_by=self.user)
        self.friend_post = Post.objects.create(body='Friend Post', created_by=self.friend)
    
    def test_post_list(self):
        url = reverse('post_list')
        response = self.client.get(url)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_in_response = any(post['body'] == 'Test Post' for post in response_data)
        friend_post_in_response = any(post['body'] == 'Friend Post' for post in response_data)
        self.assertTrue(post_in_response)
        self.assertTrue(friend_post_in_response)

    def test_post_list_profile(self):
        url = reverse('post_list_profile', args=[self.user.id])
        response = self.client.get(url)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response_data)
        self.assertIn('posts', response_data)

        user_data = response_data['user']
        self.assertEqual(user_data['id'], str(self.user.id))
        self.assertEqual(user_data['email'], self.user.email)
        self.assertEqual(user_data['name'], self.user.name)

        posts_data = response_data['posts']
        self.assertIsInstance(posts_data, list)
        self.assertTrue(any(post['body'] == 'Test Post' for post in posts_data))
        self.assertFalse(any(post['body'] == 'Friend Post' for post in posts_data))

    def test_post_create(self):
        url = reverse('post_create')
        data = {'body': 'New Post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['body'], 'New Post')
        self.assertEqual(response.json()['created_by']['name'], 'testuser')
