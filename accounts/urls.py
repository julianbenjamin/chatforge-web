from django.urls import path
from .views import settings_view
app_name = 'accounts'

urlpatterns = [
    path('settings/', settings_view, name='settings'),
]
