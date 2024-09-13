from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from post.models import Post, Trend, PostAttachment, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
import base64


User = get_user_model()

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.friend = User.objects.create_user(name='friend', email='friend@example.com', password='password')
        self.user.friends.add(self.friend)
        self.post = Post.objects.create(body='Test Post #newtrend', created_by=self.user)
        self.friend_post = Post.objects.create(body='Friend Post #newtrend', created_by=self.friend)
        self.trend = Trend.objects.create(hashtag='newtrend', occurences=2)

    def test_post_list(self):
        url = reverse('post_list')
        response = self.client.get(url)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(post['body'] == 'Test Post #newtrend' for post in response_data))
        self.assertTrue(any(post['body'] == 'Friend Post #newtrend' for post in response_data))

    def test_post_list_with_trend(self):
        url = reverse('post_list') + '?trend=newtrend'
        response = self.client.get(url)
        
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, list)
        self.assertTrue(any(post['body'] == 'Test Post #newtrend' for post in response_data))
        self.assertTrue(any(post['body'] == 'Friend Post #newtrend' for post in response_data))

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
        self.assertTrue(any(post['body'] == 'Test Post #newtrend' for post in posts_data))
        self.assertFalse(any(post['body'] == 'Friend Post #newtrend' for post in posts_data))

    def test_post_create_without_attachment(self):
        url = reverse('post_create')
        data = {'body': 'New Post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['body'], 'New Post')
        self.assertEqual(response.json()['created_by']['name'], 'testuser')

    def test_post_create_with_attachment(self):
        url = reverse('post_create')
        # Prepare an image file as attachment
        base64_image_data = (
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        image_data = base64.b64decode(base64_image_data)
        image = SimpleUploadedFile("test_image.png", image_data, content_type="image/png")
        
        data = {
            'body': 'This is a post with an attachment',
            'image': image
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(PostAttachment.objects.count(), 1)
        
        post = Post.objects.first()
        attachment = PostAttachment.objects.first()
        
        self.assertEqual(post.body, 'This is a post with an attachment')
        self.assertEqual(post.attachments.count(), 1)
        self.assertEqual(post.attachments.first(), attachment)

    def test_post_delete(self):
        self.assertTrue(Post.objects.filter(id=self.post.id).exists(), "The post should exist before deletion.")
        url = reverse('post_delete', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Post deleted')
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_post_report(self):
        url = reverse('post_report', args=[self.friend_post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'post reported')

        self.friend_post.refresh_from_db()
        self.assertIn(self.user, self.friend_post.reported_by_users.all())

    def test_get_trends(self):
        url = reverse('get_trends')
        response = self.client.get(url)
        
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, list)
        self.assertTrue(any(trend['hashtag'] == 'newtrend' for trend in response_data))

    def test_get_post_detail(self):
        url = reverse('post_detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['post']['body'], 'Test Post #newtrend')
        self.assertEqual(response.json()['post']['created_by']['name'], 'testuser')
        self.assertEqual(response.json()['post']['created_by']['email'], 'someone@example.com')

    def test_post_create_comment(self):
        url = reverse('post_create_comment', args=[self.post.id])
        data = {'body': 'This is a comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first().body, 'This is a comment')