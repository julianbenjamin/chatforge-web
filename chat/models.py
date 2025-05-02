# chat/models.py
from django.conf import settings
from django.db import models

class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    session   = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    is_user   = models.BooleanField()
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = "You" if self.is_user else "AI"
        return f"{who}: {self.content[:20]}"
