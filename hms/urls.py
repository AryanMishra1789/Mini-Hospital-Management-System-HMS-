from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('calendar/', include('calendar_integration.urls')),
    path('', include('availability.urls')),
]
