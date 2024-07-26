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
        self.post = Post.objects.create(body='Test Post', created_by=self.user)

    def test_post_list(self):
        url = reverse('post_list')
        response = self.client.get(url)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_in_response = any(post['body'] == 'Test Post' for post in response_data)
        self.assertTrue(post_in_response)

    def test_post_create(self):
        url = reverse('post_create')
        data = {'body': 'New Post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['body'], 'New Post')
        self.assertEqual(response.json()['created_by']['name'], 'testuser')
