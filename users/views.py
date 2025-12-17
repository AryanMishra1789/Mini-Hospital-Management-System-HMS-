from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm
import os
import requests
import logging

logger = logging.getLogger(__name__)


def send_signup_email(user):
    """Send welcome email to new user via serverless endpoint."""
    try:
        url = os.getenv('SERVERLESS_EMAIL_URL', 'http://localhost:3000/send')
        payload = {
            'action': 'SIGNUP_WELCOME',
            'to': user.email,
            'subject': f'Welcome to HMS - {user.get_full_name()}',
            'body': f'Hi {user.first_name},\\n\\nWelcome to the Hospital Management System!\\n\\nYou signed up as a {user.get_role_display()}.\\n\\nBest regards,\\nHMS Team'
        }
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        logger.warning(f'Failed to send signup email: {e}')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Send welcome email (non-blocking)
            send_signup_email(user)
            messages.success(request, 'Signup successful')
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def doctor_dashboard(request):
    user = request.user
    if not user.is_doctor():
        messages.error(request, 'Only doctors can access this page')
        return redirect('availability_index')
    from availability.models import TimeSlot
    from bookings.models import Booking
    slots = TimeSlot.objects.filter(doctor=user).order_by('start')[:10]
    recent_bookings = Booking.objects.filter(slot__doctor=user).order_by('-created_at')[:10]
    return render(request, 'users/doctor_dashboard.html', {
        'slots': slots,
        'recent_bookings': recent_bookings,
    })


@login_required
def patient_dashboard(request):
    user = request.user
    if not user.is_patient():
        messages.error(request, 'Only patients can access this page')
        return redirect('availability_index')
    from bookings.models import Booking
    my_bookings = Booking.objects.filter(patient=user).order_by('-created_at')[:10]
    return render(request, 'users/patient_dashboard.html', {
        'my_bookings': my_bookings,
    })
