# chat/urls.py
from django.urls import path
from .views import *

app_name = "chat"

# chat/urls.py
urlpatterns = [
    path("",            session_list,   name="session_list"),
    path("new/",          new_session,    name="session_new"),
    path("<int:pk>/rename/",  rename_session,   name="session_rename"),  # eklendi
    path("<int:pk>/delete/",  delete_session,   name="session_delete"),  # eklendi
    path("<int:pk>/",   session_detail, name="session_detail"),
    path("<int:session_id>/send/", send_message, name="send_message"),
]

