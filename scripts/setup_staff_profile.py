import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.staff_mgmt.models import StaffProfile
from datetime import date

def setup_profile():
    users = User.objects.filter(is_superuser=True)
    if not users.exists():
        print("No superuser found. Please create one first.")
        return

    admin_user = users.first()
    print(f"Checking profile for user: {admin_user.username}")

    profile, created = StaffProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'employee_id': 'ADMIN001',
            'department': 'Administration',
            'designation': 'System Administrator',
            'joining_date': date.today()
        }
    )

    if created:
        print(f"Created StaffProfile for {admin_user.username}")
    else:
        print(f"StaffProfile already exists for {admin_user.username}")

if __name__ == '__main__':
    setup_profile()
