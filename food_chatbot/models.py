from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    session_key = models.CharField(max_length=40, unique=True, null=True)
    favorite_foods = models.JSONField(default=dict)


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

