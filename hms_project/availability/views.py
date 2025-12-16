from datetime import date
from django.http import HttpResponse
from .models import TimeSlot
from users.permissions import doctor_required

@doctor_required
def create_slot(request):
    if request.method == 'POST':
        if request.POST['date'] < str(date.today()):
            return HttpResponse("Cannot create past slots")

        TimeSlot.objects.create(
            doctor=request.user,
            date=request.POST['date'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time']
        )
        return HttpResponse("Slot created successfully")
