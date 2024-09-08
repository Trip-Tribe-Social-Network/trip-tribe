from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from notification.models import Notification
from account.models import User
from post.models import Post

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.other_user = User.objects.create_user(name='otheruser', email='others@example.com', password='password')

        self.post = Post.objects.create(body='Test Post', created_by=self.other_user)

        self.notification = Notification.objects.create(
            body="Test notification",
            type_of_notification=Notification.POST_LIKE,
            created_by=self.other_user,
            created_for=self.user,
            post=self.post
        )

        self.client = APIClient()
        self.client.login(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
    
    def test_get_notifications(self):
        url = reverse('notifications')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], str(self.notification.id))
        self.assertEqual(response.json()[0]['type_of_notification'], 'post_like')

    def test_read_notification(self):
        url = reverse('read_notification', kwargs={'pk': self.notification.pk})
        response = self.client.post(url)

        self.notification.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.notification.is_read)
        self.assertEqual(response.json()['message'], 'Notification read')