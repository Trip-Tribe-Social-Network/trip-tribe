import django
import os
import sys
from datetime import timedelta
from django.utils import timezone
from collections import Counter


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trip_tribe.settings")
django.setup()


from post.models import Post, Trend

def extract_hashtags(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])

    return trends

# To avoid duplicates, delete all trends before creating new ones
for trend in Trend.objects.all():
    print(f'Deleting {trend}')
    trend.delete()

trends = []
this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)

for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    print(f'Processing post: {post}')
    extract_hashtags(post.body, trends)

for trend in Counter(trends).most_common(10):
    top_trend= Trend.objects.create(hashtag=trend[0], occurences=trend[1])
    print(top_trend)

