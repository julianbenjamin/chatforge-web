# chat/urls.py
from django.urls import path
from .views import session_list, session_detail, send_message

app_name = "chat"

# chat/urls.py
urlpatterns = [
    path("",            session_list,   name="session_list"),
    path("<int:pk>/",   session_detail, name="session_detail"),
    path("<int:session_id>/send/", send_message, name="send_message"),
]

