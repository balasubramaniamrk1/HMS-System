from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import StaffProfile, Attendance

@receiver(user_logged_in)
def auto_check_in(sender, user, request, **kwargs):
    """
    Automatically check in staff members (excluding doctors) when they log in.
    """
    # 1. Skip for Doctors
    if hasattr(user, 'doctor_profile') or user.groups.filter(name='Doctors').exists():
        return

    # 2. Ensure StaffProfile exists
    if not hasattr(user, 'staff_profile'):
        try:
            StaffProfile.objects.create(
                user=user,
                employee_id=f"EMP{user.id:04d}",
                department="General",
                designation="Staff",
                joining_date=timezone.now().date()
            )
            user.refresh_from_db()
        except Exception:
            pass

    if hasattr(user, 'staff_profile'):
        profile = user.staff_profile
        today = timezone.now().date()
        
        # 3. Check for OPEN session
        open_session = Attendance.objects.filter(staff=profile, date=today, check_out__isnull=True).exists()
        
        if not open_session:
            # Create a NEW session (Auto Check-in)
            Attendance.objects.create(
                staff=profile,
                date=today,
                check_in=timezone.now().time(),
                status='present'
            )
            # Optional: Log or message? Messages might be hard to attach to signal request properly sometimes, but usually works if request available.
            # But the user will see the widget "Currently Working" state immediately.
