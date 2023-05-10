from django.contrib.auth.models import User
from django.db import models


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_to_user')


class Friendship(models.Model):
    friend_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_friend_1')
    friend_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_friend_2')
