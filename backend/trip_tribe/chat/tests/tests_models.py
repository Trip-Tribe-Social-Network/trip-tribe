from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.models import Conversation, ConversationMessage

User = get_user_model()

class ConversationModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(name='user2', email='user2@example.com', password='password')

        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)

    def test_conversation_creation(self):
        self.assertTrue(isinstance(self.conversation, Conversation))
        self.assertEqual(str(self.conversation), f'Conversation object ({self.conversation.id})')

    def test_conversation_users(self):
        users = self.conversation.users.all()
        self.assertEqual(users.count(), 2)
        self.assertIn(self.user1, users)
        self.assertIn(self.user2, users)

    def test_conversation_modified_at_formatted(self):
        formatted_time = self.conversation.modified_at_formatted()
        
        self.assertIsInstance(formatted_time, str)        
        self.assertIn("minute", formatted_time)
        self.assertTrue(formatted_time[0].isdigit())

class ConversationMessageModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(name='user2', email='user2@example.com', password='password')

        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)

        self.message = ConversationMessage.objects.create(
            conversation=self.conversation,
            body='Hello, world!',
            sent_to=self.user2,
            created_by=self.user1
        )

    def test_message_creation(self):
        self.assertTrue(isinstance(self.message, ConversationMessage))
        self.assertEqual(str(self.message), f'ConversationMessage object ({self.message.id})')

    def test_message_fields(self):
        self.assertEqual(self.message.body, 'Hello, world!')
        self.assertEqual(self.message.sent_to, self.user2)
        self.assertEqual(self.message.created_by, self.user1)
        self.assertEqual(self.message.conversation, self.conversation)

    def test_message_created_at_formatted(self):
        formatted_time = self.message.created_at_formatted()
        self.assertIsInstance(formatted_time, str)
        self.assertIn("minute", formatted_time)
        self.assertTrue(formatted_time[0].isdigit())