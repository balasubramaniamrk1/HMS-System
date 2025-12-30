from django import forms
from .models import Equipment, MaintenanceContract, Vendor, Consumable, MaintenanceLog
from apps.core.validators import validate_phone_number
from apps.core.validators import validate_phone_number

class VendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vendor
        fields = ['name', 'contact_person', 'phone', 'email', 'website', 'address', 'rating']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_phone_number(phone)
        return phone

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_phone_number(phone)
        return phone

class EquipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Equipment
        fields = ['name', 'category', 'serial_number', 'barcode_data', 'model_number', 'manufacturer', 
                 'vendor', 'purchase_date', 'warranty_expiry', 'cost', 'useful_life', 
                 'location', 'status', 'image']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

class AMCForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = MaintenanceContract
        fields = ['equipment', 'vendor', 'contract_start', 'contract_end', 'cost', 'support_contact', 'terms']
        widgets = {
            'contract_start': forms.DateInput(attrs={'type': 'date'}),
            'contract_end': forms.DateInput(attrs={'type': 'date'}),
            'terms': forms.Textarea(attrs={'rows': 3}),
        }

class ConsumableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Consumable
        fields = ['name', 'category', 'vendor', 'barcode_data', 'quantity_in_stock', 'minimum_stock_level', 'unit', 'cost_per_unit']

class MaintenanceLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = MaintenanceLog
        fields = ['equipment', 'date', 'performed_by', 'description', 'cost']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
