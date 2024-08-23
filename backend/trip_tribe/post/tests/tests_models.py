from django.test import TestCase
from django.contrib.auth import get_user_model
from post.models import Post, PostAttachment, Trend
import uuid

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.reporter1 = User.objects.create_user(name='reporter1', email='reporter1@example.com', password='password')
        self.reporter2 = User.objects.create_user(name='reporter2', email='reporter2@example.com', password='password')
        self.post = Post.objects.create(body='Test Post', created_by=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.body, 'Test Post')
        self.assertEqual(self.post.created_by, self.user)
        self.assertTrue(isinstance(self.post.id, uuid.UUID))

    def test_post_reported_by_users(self):
        self.post.reported_by_users.add(self.reporter1, self.reporter2)
        
        self.assertIn(self.reporter1, self.post.reported_by_users.all(), "Reporter1 should have reported the post.")
        self.assertIn(self.reporter2, self.post.reported_by_users.all(), "Reporter2 should have reported the post.")
        self.assertEqual(self.post.reported_by_users.count(), 2, "The post should be reported by 2 users.")


class PostAttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.attachment = PostAttachment.objects.create(image='path/to/image.jpg', created_by=self.user)

    def test_post_attachment_creation(self):
        self.assertEqual(self.attachment.image, 'path/to/image.jpg')
        self.assertEqual(self.attachment.created_by, self.user)
        self.assertTrue(isinstance(self.attachment.id, uuid.UUID))

class TrendModelTest(TestCase):
    def setUp(self):
        self.trend = Trend.objects.create(hashtag='newtrend', occurences=10)
    
    def test_trend_creation(self):
        self.assertEqual(self.trend.hashtag, 'newtrend')
        self.assertEqual(self.trend.occurences, 10)
    
    def test_trend_occurences_update(self):
        self.trend.occurences = 20
        self.trend.save()
        
        self.trend.refresh_from_db()
        self.assertEqual(self.trend.occurences, 20)