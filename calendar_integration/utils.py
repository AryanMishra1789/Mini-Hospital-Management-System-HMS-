import os
import logging
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import GoogleCalendarToken

logger = logging.getLogger(__name__)


def get_calendar_service(user):
    """Get Google Calendar service for a user."""
    try:
        token = GoogleCalendarToken.objects.get(user=user)
        creds = Credentials(
            token=token.access_token,
            refresh_token=token.refresh_token,
            token_uri=token.token_uri,
            client_id=token.client_id,
            client_secret=token.client_secret,
            scopes=token.scopes
        )
        
        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Update stored token
            token.access_token = creds.token
            if creds.expiry:
                token.expiry = creds.expiry
            token.save()
        
        return build('calendar', 'v3', credentials=creds)
    except GoogleCalendarToken.DoesNotExist:
        logger.warning(f'No calendar token found for user {user.username}')
        return None
    except Exception as e:
        logger.error(f'Error getting calendar service: {e}')
        return None


def create_calendar_event(user, summary, start_time, end_time, description=''):
    """Create a calendar event for a user."""
    service = get_calendar_service(user)
    if not service:
        logger.warning(f'Cannot create calendar event for {user.username} - no token')
        return None
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f'Calendar event created for {user.username}: {event.get("htmlLink")}')
        return event
    except HttpError as error:
        logger.error(f'Failed to create calendar event: {error}')
        return None


def create_appointment_events(booking):
    """Create calendar events for both doctor and patient after booking."""
    doctor = booking.slot.doctor
    patient = booking.patient
    start_time = booking.slot.start
    end_time = booking.slot.end
    
    # Create event for doctor
    doctor_summary = f'Appointment with {patient.get_full_name()}'
    doctor_desc = f'Patient: {patient.get_full_name()} ({patient.email})'
    create_calendar_event(doctor, doctor_summary, start_time, end_time, doctor_desc)
    
    # Create event for patient
    patient_summary = f'Appointment with Dr. {doctor.get_full_name()}'
    patient_desc = f'Doctor: {doctor.get_full_name()} ({doctor.email})'
    create_calendar_event(patient, patient_summary, start_time, end_time, patient_desc)
