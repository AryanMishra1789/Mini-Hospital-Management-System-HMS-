from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DOCTOR = 'doctor'
    PATIENT = 'patient'
    ROLE_CHOICES = [
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PATIENT)

    def is_doctor(self):
        return self.role == self.DOCTOR

    def is_patient(self):
        return self.role == self.PATIENT
