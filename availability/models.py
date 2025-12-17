from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeSlot(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timeslots')
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        status = 'booked' if self.is_booked else 'free'
        return f"{self.doctor.username}: {self.start.isoformat()} - {self.end.isoformat()} ({status})"

    @property
    def is_future(self):
        return self.start > timezone.now()

    @classmethod
    def available_for_doctor(cls, doctor):
        return cls.objects.filter(doctor=doctor, is_booked=False, start__gt=timezone.now()).order_by('start')
