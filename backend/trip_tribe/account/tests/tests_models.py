from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import FriendshipRequest

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='Test User', email='testuser@example.com', password='password')

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_add_friends(self):
        friend1 = User.objects.create_user(name='Friend One', email='friend1@example.com', password='password')
        friend2 = User.objects.create_user(name='Friend Two', email='friend2@example.com', password='password')

        self.user.friends.add(friend1, friend2)

        self.assertIn(friend1, self.user.friends.all())
        self.assertIn(friend2, self.user.friends.all())
        self.assertEqual(self.user.friends.count(), 2)  

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(name='No Email', email='', password='password')
        
        self.assertEqual(str(context.exception), 'You have not provided a valid e-mail address')

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(name='Super User', email='superuser@example.com', password='password')
        self.assertEqual(superuser.name, 'Super User')
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.check_password('password'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class FriendshipRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='User One', email='userone@example.com', password='password')
        self.user2 = User.objects.create_user(name='User Two', email='usertwo@example.com', password='password')

    def test_friendship_request_creation(self):
        request = FriendshipRequest.objects.create(
            created_for=self.user2,
            created_by=self.user1
        )

        self.assertEqual(FriendshipRequest.objects.count(), 1)
        self.assertEqual(request.created_for, self.user2)
        self.assertEqual(request.created_by, self.user1)
        self.assertEqual(request.status, FriendshipRequest.SENT)

    def test_status_choices(self):
        request = FriendshipRequest.objects.create(
            created_for=self.user2,
            created_by=self.user1,
            status=FriendshipRequest.ACCEPTED
        )

        self.assertEqual(request.status, FriendshipRequest.ACCEPTED)

        request.status = FriendshipRequest.REJECTED
        request.save()
        self.assertEqual(request.status, FriendshipRequest.REJECTED)

    def test_related_name(self):
        request = FriendshipRequest.objects.create(
            created_for=self.user2,
            created_by=self.user1
        )

        self.assertIn(request, self.user1.created_friendshiprequests.all())
        self.assertIn(request, self.user2.received_friendshiprequests.all())