from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='availability_index'),
    path('my-slots/', views.my_slots, name='my_slots'),
    path('create-slot/', views.create_slot, name='create_slot'),
]
