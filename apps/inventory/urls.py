from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.amc_expiry_dashboard, name='inventory_dashboard'),
    
    # Equipment
    path('list/', views.inventory_list, name='inventory_list'),
    path('equipment/add/', views.add_equipment, name='add_equipment'),
    path('equipment/<int:pk>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<int:pk>/qr/', views.view_qr, name='view_qr'),
    
    # Maintenance Logs
    path('equipment/<int:equipment_id>/logs/', views.maintenance_log_list, name='maintenance_log_list'),
    path('equipment/<int:equipment_id>/logs/add/', views.add_maintenance_log, name='add_maintenance_log'),

    # AMC
    path('amc/list/', views.amc_list, name='amc_list'),
    path('amc/add/', views.add_amc, name='add_amc'),
    path('amc/<int:pk>/edit/', views.edit_amc, name='edit_amc'),

    # Vendor Management
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/add/', views.add_vendor, name='add_vendor'),
    path('vendors/<int:pk>/edit/', views.edit_vendor, name='edit_vendor'),

    # Consumables
    path('consumables/', views.consumable_list, name='consumable_list'),
    path('consumables/add/', views.add_consumable, name='add_consumable'),
    path('consumables/<int:pk>/edit/', views.edit_consumable, name='edit_consumable'),
]
