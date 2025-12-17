from django.db import models
from django.conf import settings


class GoogleCalendarToken(models.Model):
    """Stores Google Calendar OAuth2 tokens for users."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendar_token')
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.URLField()
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.JSONField()
    expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Calendar token for {self.user.username}"
