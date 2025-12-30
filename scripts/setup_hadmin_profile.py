import os
import sys
import django
from datetime import date

# Set up path so 'apps' can be found
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps')) # Add apps directory to path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')

django.setup()

from django.contrib.auth.models import User
from staff_mgmt.models import StaffProfile, Shift

def setup_hadmin_profile():
    try:
        user = User.objects.get(username='hadmin')
        
        # Create a default admin shift if not exists
        shift, _ = Shift.objects.get_or_create(
            name='General',
            defaults={
                'start_time': '09:00:00',
                'end_time': '18:00:00'
            }
        )
        
        # Create Profile
        profile, created = StaffProfile.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': 'HA001',
                'department': 'Administration',
                'designation': 'Hospital Admin',
                'joining_date': date.today(),
                'shift': shift
            }
        )
        
        if created:
            print("StaffProfile created for 'hadmin'.")
        else:
            print("StaffProfile already exists for 'hadmin'.")
            
    except User.DoesNotExist:
        print("User 'hadmin' does not exist. Please run setup_hospital_admin.py first.")

if __name__ == '__main__':
    setup_hadmin_profile()
