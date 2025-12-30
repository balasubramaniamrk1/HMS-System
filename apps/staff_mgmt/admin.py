from django.contrib import admin
from .models import StaffProfile, Attendance, Shift

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation', 'shift')
    search_fields = ('user__username', 'user__first_name', 'employee_id')
    list_filter = ('department', 'shift')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'check_in', 'check_out', 'status', 'is_late')
    list_filter = ('status', 'is_late', 'date', 'staff__department')
    date_hierarchy = 'date'
