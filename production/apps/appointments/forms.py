from django import forms
from .models import AppointmentRequest
from apps.core.validators import validate_phone_number

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ['name', 'phone', 'email', 'department', 'doctor', 'preferred_date', 'preferred_time', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (Optional)'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'preferred_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Morning / Evening etc.'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any specific problem or request?'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_phone_number(phone)
        return phone
