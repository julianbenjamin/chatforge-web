from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    openrouter_api_key = models.CharField(max_length=128, blank=True)
    default_model = models.CharField(max_length=50, default="gpt-4.1-mini")

class AIModel(models.Model):
    model_id   = models.CharField(max_length=100, unique=True)
    name       = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

