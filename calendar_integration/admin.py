from django.contrib import admin
from .models import GoogleCalendarToken


@admin.register(GoogleCalendarToken)
class GoogleCalendarTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiry', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
