from django.urls import path
from .views import register_participant
urlpatterns = [
    path('register/', register_participant, name='register_participant'),
]