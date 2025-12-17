from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from .models import GoogleCalendarToken
import os


SCOPES = ['https://www.googleapis.com/auth/calendar']


@login_required
def google_calendar_auth(request):
    """Initiate Google Calendar OAuth2 flow."""
    # This requires a client_secrets.json file with OAuth2 credentials
    # Users must create this from Google Cloud Console
    client_secrets_file = os.path.join(settings.BASE_DIR, 'client_secrets.json')
    
    if not os.path.exists(client_secrets_file):
        messages.error(request, 'Google Calendar OAuth not configured. Please add client_secrets.json')
        return redirect('/')
    
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=SCOPES,
        redirect_uri=request.build_absolute_uri('/calendar/oauth2callback/')
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    request.session['state'] = state
    return redirect(authorization_url)


@login_required
def google_calendar_callback(request):
    """Handle OAuth2 callback and store credentials."""
    state = request.session.get('state')
    
    client_secrets_file = os.path.join(settings.BASE_DIR, 'client_secrets.json')
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=SCOPES,
        state=state,
        redirect_uri=request.build_absolute_uri('/calendar/oauth2callback/')
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    
    # Store credentials
    GoogleCalendarToken.objects.update_or_create(
        user=request.user,
        defaults={
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry': credentials.expiry,
        }
    )
    
    messages.success(request, 'Google Calendar connected successfully')
    return redirect('/')
