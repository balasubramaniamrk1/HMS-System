from django.db import models
from django.contrib.auth.models import User

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'On Leave'),
    )
    
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    is_late = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date', '-check_in']
    
    def __str__(self):
        return f"{self.staff} - {self.date}"

    @property
    def work_hours(self):
        if self.check_in and self.check_out:
            # Convert to dummy datetime for subtraction (since time objects can't be subtracted directly)
            from datetime import datetime, date
            dummy_date = date.today()
            start = datetime.combine(dummy_date, self.check_in)
            end = datetime.combine(dummy_date, self.check_out)
            diff = end - start
            hours = diff.total_seconds() / 3600
            return f"{hours:.1f} hrs"
        return "-"
