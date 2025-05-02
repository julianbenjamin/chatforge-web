# chat/admin.py
from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("session", "is_user", "timestamp")
    list_filter  = ("is_user",)
