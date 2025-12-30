import os
import sys
import django
from datetime import time, date

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.staff_mgmt.models import StaffProfile, Shift

def setup_shift_and_profile():
    users = User.objects.filter(is_superuser=True)
    if not users.exists():
        print("No superuser found.")
        return

    admin_user = users.first()
    
    # 1. Create Shift
    morning_shift, _ = Shift.objects.get_or_create(
        name="Morning Shift",
        defaults={
            'start_time': time(9, 0), # 9:00 AM
            'end_time': time(17, 0)   # 5:00 PM
        }
    )
    print(f"Shift ensured: {morning_shift}")

    # 2. Assign Shift to Profile
    profile, created = StaffProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'employee_id': 'ADMIN001',
            'department': 'Administration',
            'designation': 'System Administrator',
            'joining_date': date.today()
        }
    )
    
    if profile.shift != morning_shift:
        profile.shift = morning_shift
        profile.save()
        print(f"Assigned '{morning_shift}' to {profile}")
    else:
        print(f"Profile {profile} already has '{morning_shift}'")

if __name__ == '__main__':
    setup_shift_and_profile()
