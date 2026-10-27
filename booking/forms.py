from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # We only want the user to fill these out. 
        # Status, Reference No, and User are handled by the system automatically.
        fields = ['room', 'date', 'start_time', 'end_time', 'purpose']
        
        # Add some basic CSS classes to make the form look decent
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }