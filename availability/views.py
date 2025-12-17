from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TimeSlot
from .forms import TimeSlotForm
from django.contrib import messages


def index(request):
    """List all doctors and their upcoming available slots."""
    doctors = []
    from users.models import User
    doctors_qs = User.objects.filter(role=User.DOCTOR)
    for d in doctors_qs:
        slots = TimeSlot.available_for_doctor(d)[:10]
        doctors.append({'doctor': d, 'slots': slots})
    return render(request, 'availability/index.html', {'doctors': doctors})


@login_required
def my_slots(request):
    """Doctor dashboard to view their own time slots."""
    user = request.user
    if not user.is_doctor():
        messages.error(request, 'Only doctors can access this page')
        return redirect('availability_index')
    slots = TimeSlot.objects.filter(doctor=user).order_by('start')
    return render(request, 'availability/my_slots.html', {'slots': slots})


@login_required
def create_slot(request):
    """Doctor creates a new time slot."""
    user = request.user
    if not user.is_doctor():
        messages.error(request, 'Only doctors can create slots')
        return redirect('availability_index')

    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = user
            slot.save()
            messages.success(request, 'Time slot created')
            return redirect('my_slots')
    else:
        form = TimeSlotForm()
    return render(request, 'availability/create_slot.html', {'form': form})
