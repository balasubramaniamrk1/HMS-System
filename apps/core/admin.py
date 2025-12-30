from django.contrib import admin
from .models import HealthPackage, ContactMessage, CareerApplication

@admin.register(HealthPackage)
class HealthPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discounted_price', 'is_active')
    list_editable = ('price', 'discounted_price', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at')
    list_filter = ('subject', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'created_at')
    list_filter = ('position',)
    readonly_fields = ('created_at',)
