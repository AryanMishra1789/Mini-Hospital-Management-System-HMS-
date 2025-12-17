from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.google_calendar_auth, name='calendar_auth'),
    path('oauth2callback/', views.google_calendar_callback, name='calendar_callback'),
]
