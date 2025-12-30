from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile, Shift
from doctors.models import Doctor, Department
from core.models import HealthPackage, GalleryImage

class StaffUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class StaffUserChangeForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['employee_id', 'department', 'designation', 'joining_date', 'shift']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'qualifications', 'specialization', 'bio', 'experience_years', 'is_featured', 'photo']
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'icon']

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['name', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class HealthPackageForm(forms.ModelForm):
    class Meta:
        model = HealthPackage
        fields = ['name', 'price', 'discounted_price', 'inclusions', 'image', 'is_active']
        widgets = {
            'inclusions': forms.Textarea(attrs={'rows': 4, 'placeholder': 'List items separated by new lines'}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption']
