from django.test import TestCase
from django.contrib.auth import get_user_model
from post.models import Post, PostAttachment
import uuid

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.post = Post.objects.create(body='Test Post', created_by=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.body, 'Test Post')
        self.assertEqual(self.post.created_by, self.user)
        self.assertTrue(isinstance(self.post.id, uuid.UUID))

class PostAttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='someone@example.com', password='password')
        self.attachment = PostAttachment.objects.create(image='path/to/image.jpg', created_by=self.user)

    def test_post_attachment_creation(self):
        self.assertEqual(self.attachment.image, 'path/to/image.jpg')
        self.assertEqual(self.attachment.created_by, self.user)
        self.assertTrue(isinstance(self.attachment.id, uuid.UUID))
