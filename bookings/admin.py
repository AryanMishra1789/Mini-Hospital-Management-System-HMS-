from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('slot', 'patient', 'created_at')
    search_fields = ('patient__username', 'slot__doctor__username')
