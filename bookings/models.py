from django.db import models, transaction
from django.conf import settings
from availability.models import TimeSlot


class Booking(models.Model):
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='booking')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.patient.username} with {self.slot}"

    @classmethod
    def create_for_slot(cls, slot_id, patient):
        """Atomically create a booking for a timeslot if it's not already booked."""
        with transaction.atomic():
            slot = TimeSlot.objects.select_for_update().get(pk=slot_id)
            if slot.is_booked:
                raise ValueError('Slot already booked')
            slot.is_booked = True
            slot.save()
            booking = cls.objects.create(slot=slot, patient=patient)
            return booking
