from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.models import User
from post.models import Post

class SearchAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.other_user1 = User.objects.create_user(name='Alice', email='alice@example.com', password='password')
        self.other_user2 = User.objects.create_user(name='Bob', email='bob@example.com', password='password')

        self.client.force_authenticate(user=self.user)

        self.post1 = Post.objects.create(body='Alice first post', created_by=self.other_user1)
        self.post2 = Post.objects.create(body='Bob is here', created_by=self.other_user2)
        
    def test_search_successful(self):
        url = reverse('search')
        data = {'query': 'Alice'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        self.assertEqual(len(response_data['users']), 1)
        self.assertEqual(response_data['users'][0]['name'], 'Alice')
        
        self.assertEqual(len(response_data['posts']), 1)
        self.assertEqual(response_data['posts'][0]['body'], 'Alice first post')
    
    def test_search_no_matches(self):
        url = reverse('search')
        data = {'query': 'Nonexistent'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        self.assertEqual(response_data['users'], [])
        self.assertEqual(response_data['posts'], [])
