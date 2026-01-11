from django.utils import timezone
from .models import StaffProfile, Attendance
import datetime

def attendance_context(request):
    """
    Provides attendance data for the global check-in widget.
    Auto-creates StaffProfile for authenticated users if missing.
    """
    if not request.user.is_authenticated:
        return {}

    # Skip for Doctors (they have their own console logic/don't use this widget)
    if hasattr(request.user, 'doctor_profile') or request.user.groups.filter(name='Doctors').exists():
        return {'is_doctor': True}

    # Auto-create StaffProfile if missing
    if not hasattr(request.user, 'staff_profile'):
        try:
            StaffProfile.objects.create(
                user=request.user,
                employee_id=f"EMP{request.user.id:04d}",
                department="General",
                designation="Staff",
                joining_date=timezone.now().date()
            )
            request.user.refresh_from_db()
        except Exception:
            # Handle potential race conditions or DB errors gracefully
            pass

    todays_attendance = None
    work_duration = "-- : --"
    staff_initials = ""
    staff_name = ""
    staff_designation = ""
    profile = None

    try:
        if hasattr(request.user, 'staff_profile'):
            profile = request.user.staff_profile
            staff_name = profile.user.get_full_name()
            staff_designation = profile.designation
            
            fname = profile.user.first_name if profile.user.first_name else ""
            lname = profile.user.last_name if profile.user.last_name else ""
            staff_initials = (fname[:1] + lname[:1]).upper()

            today = timezone.now().date()
            all_sessions = Attendance.objects.filter(staff=profile, date=today)
            todays_attendance = all_sessions.filter(check_out__isnull=True).last()
            
            # If no open session, use last closed one
            if not todays_attendance:
                todays_attendance = all_sessions.last()
            
            # Calculate total duration
            total_seconds = 0
            for session in all_sessions:
                if session.check_in:
                    start_dt = datetime.datetime.combine(today, session.check_in)
                    if session.check_out:
                        end_dt = datetime.datetime.combine(today, session.check_out)
                    else:
                        end_dt = datetime.datetime.combine(today, timezone.now().time())
                    
                    if end_dt >= start_dt:
                        total_seconds += int((end_dt - start_dt).total_seconds())

            if total_seconds > 0:
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                work_duration = f"{hours}h {minutes}m"

    except Exception as e:
        print(f"Error in attendance_context: {e}")

    return {
        'attendance_widget': {
            'todays_attendance': todays_attendance,
            'work_duration': work_duration,
            'staff_initials': staff_initials,
            'staff_name': staff_name,
            'staff_designation': staff_designation,
            'has_profile': profile is not None
        },
        'is_doctor': False
    }
