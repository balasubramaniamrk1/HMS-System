from django.contrib import admin
from .models import EquipmentCategory, Equipment, MaintenanceContract

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'category', 'location', 'status', 'warranty_expiry')
    list_filter = ('status', 'category', 'location')
    search_fields = ('name', 'serial_number')

@admin.register(MaintenanceContract)
class MaintenanceContractAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'provider_name', 'contract_end', 'cost')
    list_filter = ('provider_name', 'contract_end')
    date_hierarchy = 'contract_end'
