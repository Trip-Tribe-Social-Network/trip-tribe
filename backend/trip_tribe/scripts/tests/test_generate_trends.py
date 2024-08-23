from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from post.models import Post, Trend
from django.contrib.auth import get_user_model

User = get_user_model()

class GenerateTrendsTestCase(TestCase):
    def setUp(self):
        # Create mock posts with hashtags
        self.user = User.objects.create_user(name='TestUser', email='test@example.com', password='password')
        Post.objects.create(body="#hashtag1 #hashtag2", created_by=self.user)
        Post.objects.create(body="#hashtag1", created_by=self.user)

    def test_generate_trends(self):
        self.assertEqual(Trend.objects.count(), 0)
        
        # Manually run the script logic within the test case
        trends = []
        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        twenty_four_hours = this_hour - timedelta(hours=24)

        for post in Post.objects.filter(created_at__gte=twenty_four_hours):
            self.extract_hashtags(post.body, trends)

        for trend in Counter(trends).most_common(10):
            Trend.objects.create(hashtag=trend[0], occurences=trend[1])

        # Check that trends were created
        self.assertEqual(Trend.objects.count(), 2)
        trend1 = Trend.objects.get(hashtag='hashtag1')
        trend2 = Trend.objects.get(hashtag='hashtag2')
        self.assertEqual(trend1.occurences, 2)
        self.assertEqual(trend2.occurences, 1)

    def extract_hashtags(self, text, trends):
        for word in text.split():
            if word[0] == '#':
                trends.append(word[1:])
        return trends
