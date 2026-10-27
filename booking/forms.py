from django import forms
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            # Add 'min': today to the date widget here
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().date().isoformat()}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # 1. Prevent Past Dates
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot book a room for a date in the past.")

        if start_time and end_time:
            # 2. Prevent Overnight/Mixed-up bookings
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after the start time.")
            
            # 3. Limit to 4 hours max
            from datetime import datetime
            start_dt = datetime.combine(date, start_time)
            end_dt = datetime.combine(date, end_time)
            duration = end_dt - start_dt
            
            if duration.total_seconds() > 4 * 3600:
                raise forms.ValidationError("You cannot book a room for more than 4 hours at a time.")
        
        return cleaned_data