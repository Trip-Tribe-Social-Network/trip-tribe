from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from chat.models import Conversation, ConversationMessage
from chat.serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer

User = get_user_model()

class ConversationAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(name='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(name='user2', email='user2@example.com', password='password')
        self.user3 = User.objects.create_user(name='user3', email='user3@example.com', password='password')
        
        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)
        
        self.client = APIClient()
        self.client.login(email='user1@example.com', password='password')
        self.client.force_authenticate(user=self.user1)

    def test_conversation_list(self):
        url = reverse('conversation_list')
        response = self.client.get(url)

        conversations = Conversation.objects.filter(users__in=[self.user1])
        serializer = ConversationSerializer(conversations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_conversation_detail(self):
        url = reverse('conversation_detail', args=[self.conversation.pk])
        response = self.client.get(url)

        serializer = ConversationDetailSerializer(self.conversation)
        response_data = response.json()
        expected_data = serializer.data

        # Convert UUID fields in the expected data to strings for comparison
        expected_data['users'] = [str(uuid) for uuid in expected_data['users']]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], str(expected_data['id']))
        self.assertEqual(response_data['users'], expected_data['users'])

    def test_conversation_get_or_create(self):
        url = reverse('conversation_get_or_create', args=[self.user2.pk])
        response = self.client.get(url)

        conversation = Conversation.objects.get(pk=self.conversation.pk)
        serializer = ConversationDetailSerializer(conversation)

        response_data = response.json()
        expected_data = serializer.data

        expected_data['users'] = [str(uuid) for uuid in expected_data['users']]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

        # Test creating a new conversation
        self.client.logout()
        self.client.login(email='user2@example.com', password='password')
        self.client.force_authenticate(user=self.user2)
        create_url = reverse('conversation_get_or_create', args=[self.user3.pk])
        response = self.client.get(create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conversation.objects.count(), 2) 

    def test_conversation_send_message(self):
        url = reverse('conversation_send_message', args=[self.conversation.pk])
        message_data = {'body': 'Hello from user1!'}
        response = self.client.post(url, message_data, format='json')

        message = ConversationMessage.objects.first()
        serializer = ConversationMessageSerializer(message)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
