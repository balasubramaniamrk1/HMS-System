from django.contrib import admin
from .models import Ward, Bed, Admission

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward_type', 'floor')
    list_filter = ('ward_type',)

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'ward', 'status', 'price_per_day')
    list_filter = ('ward', 'status')
    search_fields = ('bed_number',)

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'bed', 'doctor', 'admission_date', 'status')
    list_filter = ('status', 'ward', 'admission_date')
    search_fields = ('patient_name', 'patient_phone')
    date_hierarchy = 'admission_date'
