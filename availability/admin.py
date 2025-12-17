from django.contrib import admin
from .models import TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start', 'end', 'is_booked')
    list_filter = ('is_booked', 'doctor')
    search_fields = ('doctor__username',)
