from django.contrib import admin
from .models import Department, Doctor

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'specialization', 'is_featured')
    list_filter = ('department', 'is_featured')
    search_fields = ('name', 'specialization')
    prepopulated_fields = {'slug': ('name',)}
