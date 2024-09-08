from django.test import TestCase
from account.models import User, FriendshipRequest
from post.models import Post
from notification.models import Notification
from notification.utils import create_notification


class CreateNotificationUtilsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='user_one', email='user_one@example.com', password='password')
        self.user2 = User.objects.create_user(name='user_two', email='user_two@example.com', password='password')
        
        self.post = Post.objects.create(body="Sample post", created_by=self.user2)
        
        self.friend_request = FriendshipRequest.objects.create(created_by=self.user1, created_for=self.user2)

    def test_create_post_like_notification(self):
        notification = create_notification(
            request=self._mock_request(self.user1), 
            type_of_notification=Notification.POST_LIKE, 
            post_id=self.post.id
        )
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.body, f'user_one liked one of your posts!')
        self.assertEqual(notification.type_of_notification, 'post_like')
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)
        self.assertEqual(notification.post, self.post)

    def test_create_post_comment_notification(self):
        notification = create_notification(
            request=self._mock_request(self.user1), 
            type_of_notification=Notification.POST_COMMENT, 
            post_id=self.post.id
        )
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.body, f'user_one commented on one of your posts!')
        self.assertEqual(notification.type_of_notification, 'post_comment')
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)
        self.assertEqual(notification.post, self.post)

    def test_create_new_friend_request_notification(self):
        notification = create_notification(
            request=self._mock_request(self.user1), 
            type_of_notification=Notification.NEW_FRIEND_REQUEST, 
            friendrequest_id=self.friend_request.id
        )
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.body, f'user_one sent you a friend request!')
        self.assertEqual(notification.type_of_notification, 'new_friendrequest')
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)

    def test_create_accepted_friend_request_notification(self):
        notification = create_notification(
            request=self._mock_request(self.user1), 
            type_of_notification=Notification.ACCPTED_FRIEND_REQUEST, 
            friendrequest_id=self.friend_request.id
        )
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.body, f'user_one accepted your friend request!')
        self.assertEqual(notification.type_of_notification, 'accepted_friendrequest')
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)

    def test_create_rejected_friend_request_notification(self):
        notification = create_notification(
            request=self._mock_request(self.user1), 
            type_of_notification=Notification.REJECTED_FRIEND_REQUEST, 
            friendrequest_id=self.friend_request.id
        )
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.body, f'{self.user1.name} rejected your friend request!')
        self.assertEqual(notification.type_of_notification, 'rejected_friendrequest')
        self.assertEqual(notification.created_by, self.user1)
        self.assertEqual(notification.created_for, self.user2)

    def _mock_request(self, user):
        class MockRequest:
            def __init__(self, user):
                self.user = user
        
        return MockRequest(user)
