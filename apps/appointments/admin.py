from django.contrib import admin
from .models import AppointmentRequest, Consultation

class ConsultationInline(admin.StackedInline):
    model = Consultation
    extra = 0

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'preferred_date', 'status')
    list_filter = ('status', 'preferred_date')
    search_fields = ('name', 'phone')
    inlines = [ConsultationInline]

