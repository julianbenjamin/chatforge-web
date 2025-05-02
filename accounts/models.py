from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    openrouter_api_key = models.CharField(max_length=200, blank=True)
    default_model      = models.CharField(max_length=100, blank=True)
    favorite_models    = models.ManyToManyField(
        'AIModel',
        blank=True,
        related_name='favorited_by',
        help_text="Kullanıcının favori modelleri"
    )

class AIModel(models.Model):
    model_id   = models.CharField(max_length=100, unique=True)
    name       = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

