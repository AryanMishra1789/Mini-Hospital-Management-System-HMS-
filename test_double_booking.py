from users.models import User
from availability.models import TimeSlot
from bookings.models import Booking

patient = User.objects.get(username='patient1')
slot = TimeSlot.objects.first()

try:
    booking = Booking.create_for_slot(slot.id, patient)
    print('ERROR: Should have raised ValueError')
except ValueError as e:
    print(f'SUCCESS: Race condition prevented - {e}')
