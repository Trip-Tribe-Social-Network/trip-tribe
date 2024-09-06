from django.db import models
from account.models import User
from post.models import Post

import uuid


class Notification(models.Model):
    NEW_FRIEND_REQUEST = 'new_friendrequest'
    ACCPTED_FRIEND_REQUEST = 'accepted_friendrequest'
    REJECTED_FRIEND_REQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEW_FRIEND_REQUEST, 'New Friend Request'),
        (ACCPTED_FRIEND_REQUEST, 'Accepted Friend Request'),
        (REJECTED_FRIEND_REQUEST, 'Rejected Friend Request'),
        (POST_LIKE, 'Post Liked'),
        (POST_COMMENT, 'Post Comment')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
