from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    openrouter_api_key = models.CharField(max_length=128, blank=True)
    default_model = models.CharField(max_length=50, default="gpt-4.1-mini")
