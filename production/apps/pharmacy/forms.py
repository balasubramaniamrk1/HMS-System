from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'barcode', 'generic_name', 'category', 'manufacturer', 'dosage_form', 'schedule_type', 'reorder_level', 'tax', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scan or Type Barcode'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Generic Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage_form': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tablet, Syrup, etc.'}),
            'schedule_type': forms.Select(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tax % (e.g. 5.00)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
