from django.test import TestCase
from account.models import User
from post.models import Post
from notification.models import Notification


class NotificationModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='user_one', email='user_one@example.com', password='password')
        self.user2 = User.objects.create_user(name='user_two', email='user_two@example.com', password='password')
        
        self.post = Post.objects.create(body="Sample post", created_by=self.user1)
        
        self.notification = Notification.objects.create(
            body="Test notification body",
            type_of_notification=Notification.POST_LIKE,
            created_by=self.user1,
            created_for=self.user2,
            post=self.post
        )

    def test_notification_creation(self):
        notification = self.notification
        self.assertEqual(notification.body, "Test notification body")
        self.assertEqual(notification.type_of_notification, 'post_like')
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)
        self.assertEqual(notification.post, self.post)

    def test_mark_notification_as_read(self):
        self.notification.is_read = True
        self.notification.save()

        self.assertTrue(self.notification.is_read)

    def test_notification_type_choices(self):
        self.assertIn(self.notification.type_of_notification, dict(Notification.CHOICES_TYPE_OF_NOTIFICATION).keys())

    def test_notification_for_friend_request(self):
        friend_request_notification = Notification.objects.create(
            body="Friend request",
            type_of_notification=Notification.NEW_FRIEND_REQUEST,
            created_by=self.user1,
            created_for=self.user2
        )
        
        self.assertEqual(friend_request_notification.type_of_notification, 'new_friendrequest')
        self.assertEqual(friend_request_notification.created_by, self.user1)
        self.assertEqual(friend_request_notification.created_for, self.user2)

    def test_accepted_friend_request_notification(self):
        accepted_friend_request_notification = Notification.objects.create(
            body="Friend request accepted",
            type_of_notification=Notification.ACCPTED_FRIEND_REQUEST,
            created_by=self.user1,
            created_for=self.user2
        )
        self.assertEqual(accepted_friend_request_notification.body, "Friend request accepted")
        self.assertEqual(accepted_friend_request_notification.type_of_notification, 'accepted_friendrequest')
        self.assertEqual(accepted_friend_request_notification.created_by, self.user1)
        self.assertEqual(accepted_friend_request_notification.created_for, self.user2)

    def test_rejected_friend_request_notification(self):
        rejected_friend_request_notification = Notification.objects.create(
            body="Friend request rejected",
            type_of_notification=Notification.REJECTED_FRIEND_REQUEST,
            created_by=self.user1,
            created_for=self.user2
        )
        self.assertEqual(rejected_friend_request_notification.body, "Friend request rejected")
        self.assertEqual(rejected_friend_request_notification.type_of_notification, 'rejected_friendrequest')
        self.assertEqual(rejected_friend_request_notification.created_by, self.user1)
        self.assertEqual(rejected_friend_request_notification.created_for, self.user2)

