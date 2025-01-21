from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

class UserAction(models.Model):
    HIDE = 'HIDE'
    BLOCK = 'BLOCK'
    ACTION_CHOICES = [
        (HIDE, 'Hide'),
        (BLOCK, 'Block'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_actions')
    action = models.CharField(max_length=5, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'target_user', 'action']

    def __str__(self):
        return f'{self.user} {self.action} {self.target_user}'
