import os
import sys
import django
from datetime import date
# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from staff_mgmt.models import StaffProfile, Shift

def create_receptionist():
    # 1. Create/Get 'Receptionist' Group
    group_name = 'Receptionist'
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Created group '{group_name}'")
    else:
        print(f"Group '{group_name}' already exists")

    # 2. Create User
    username = 'receptionist'
    password = 'password123'
    email = 'reception@healthplus.com'
    
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.email = email
        user.first_name = "Front"
        user.last_name = "Desk"
        user.save()
        print(f"Created user '{username}' with password '{password}'")
    else:
        print(f"User '{username}' already exists")

    # 3. Add to Group
    user.groups.add(group)
    print(f"Added {username} to {group_name} group")

    # 4. Create StaffProfile (Required for accessing dashboards that require is_staff_member test)
    # Also assign a shift if available
    morning_shift = Shift.objects.filter(name__icontains="Morning").first()
    
    profile, created = StaffProfile.objects.get_or_create(
        user=user,
        defaults={
            'employee_id': 'REC001',
            'department': 'Administration',
            'designation': 'Receptionist',
            'joining_date': date.today(),
            'shift': morning_shift
        }
    )
    if created:
        print(f"Created StaffProfile for {username}")
    else:
        print(f"StaffProfile already exists for {username}")

if __name__ == '__main__':
    create_receptionist()
