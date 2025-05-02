# chatforge/urls.py
from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path("",      home,                         name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("chat/",    include(("chat.urls",     "chat"),     namespace="chat")),
]
