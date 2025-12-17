from django import forms
from .models import TimeSlot


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start', 'end']

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start')
        end = cleaned.get('end')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time')
        return cleaned
