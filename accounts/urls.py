from django.urls import path
from .views import *
app_name = 'accounts'

urlpatterns = [
    path('settings/', settings_view, name='settings'),
    path('settings/refresh/', refresh_models, name='refresh_models'),
     path('favorites/', favorites_view, name='favorites'),

]
