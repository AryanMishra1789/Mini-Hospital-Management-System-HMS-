from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from availability.models import TimeSlot
from .utils import send_email_notification
from calendar_integration.utils import create_appointment_events


@login_required
def create_booking(request, slot_id):
    """Patient books a time slot."""
    user = request.user
    if not user.is_patient():
        messages.error(request, 'Only patients can book slots')
        return redirect('/')

    try:
        booking = Booking.create_for_slot(slot_id=slot_id, patient=user)
    except TimeSlot.DoesNotExist:
        messages.error(request, 'Time slot not found')
        return redirect('/')
    except ValueError:
        messages.error(request, 'Time slot already booked')
        return redirect('/')

    messages.success(request, 'Booking confirmed')
    
    # Call serverless email endpoint for patient and doctor notifications (best-effort)
    try:
        patient_email = booking.patient.email
        doctor_email = booking.slot.doctor.email
        subject = f'Appointment with Dr. {booking.slot.doctor.get_full_name()}'
        body = (
            f"Appointment confirmed:\nPatient: {booking.patient.get_full_name()}\n"
            f"Doctor: {booking.slot.doctor.get_full_name()}\nStart: {booking.slot.start}\nEnd: {booking.slot.end}"
        )
        # Fire-and-forget (we don't block booking on email success)
        send_email_notification('BOOKING_CONFIRMATION', patient_email, subject=subject, body=body)
        send_email_notification('BOOKING_CONFIRMATION', doctor_email, subject=subject, body=body)
    except Exception:
        # ignore email failures but log in server logs
        pass

    # Create Google Calendar events for both doctor and patient
    try:
        create_appointment_events(booking)
    except Exception:
        # Google Calendar is optional, don't block booking on calendar failures
        pass

    return render(request, 'bookings/booking_confirmed.html', {'booking': booking})
