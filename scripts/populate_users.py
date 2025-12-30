import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from staff_mgmt.models import StaffProfile
from doctors.models import Department, Doctor
from django.utils import timezone
import datetime

def create_users():
    print("Creating Departments...")
    cardio, _ = Department.objects.get_or_create(name="Cardiology", defaults={'description': 'Heart care'})
    ortho, _ = Department.objects.get_or_create(name="Orthopedics", defaults={'description': 'Bone care'})
    general, _ = Department.objects.get_or_create(name="General Medicine", defaults={'description': 'General care'})
    admin_dept, _ = Department.objects.get_or_create(name="Administration", defaults={'description': 'Admin stuff'})

    users_data = [
        {
            "username": "receptionist", "email": "frontdesk@hms.com", "password": "password123",
            "first_name": "Ramesh", "last_name": "Kumar",
            "role": "Receptionist", "dept": "Administration", "emp_id": "EMP001"
        },
        {
            "username": "nurse_mary", "email": "mary@hms.com", "password": "password123",
            "first_name": "Mary", "last_name": "Joseph",
            "role": "Nurse", "dept": "General Medicine", "emp_id": "EMP002"
        },
        {
            "username": "inventory_mgr", "email": "store@hms.com", "password": "password123",
            "first_name": "Suresh", "last_name": "Raina",
            "role": "Inventory Manager", "dept": "Administration", "emp_id": "EMP003"
        },
        {
            "username": "dr_ariva", "email": "ariva@hms.com", "password": "password123",
            "first_name": "Arivalagan", "last_name": "M",
            "role": "Doctor", "dept": "Cardiology", "emp_id": "DOC001"
        }
    ]

    print("Creating Users and Staff Profiles...")
    for data in users_data:
        user, created = User.objects.get_or_create(username=data['username'], defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name']
        })
        
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"User {user.username} created.")
        else:
            print(f"User {user.username} already exists.")

        # Create/Update Staff Profile
        if hasattr(user, 'staff_profile'):
             print(f"StaffProfile for {user.username} already exists.")
        elif StaffProfile.objects.filter(employee_id=data['emp_id']).exists():
             print(f"Skipping {user.username}: Employee ID {data['emp_id']} already taken.")
        else:
            StaffProfile.objects.create(
                user=user,
                employee_id=data['emp_id'],
                department=data['dept'],
                designation=data['role'],
                joining_date=timezone.now().date()
            )
            print(f"StaffProfile for {user.username} created.")

    print("Creating Doctors (Public Profiles)...")
    # Note: These are public profiles separate from Users for now
    Doctor.objects.get_or_create(
        name="Dr. Arivalagan M",
        defaults={
            'department': cardio, 
            'qualifications': 'MBBS, MD', 
            'specialization': 'Interventional Cardiology',
            'experience_years': 15,
            'bio': 'Senior Cardiologist with 15 years experience.'
        }
    )
    Doctor.objects.get_or_create(
        name="Dr. Saravanan",
        defaults={
            'department': ortho, 
            'qualifications': 'MBBS, MS (Ortho)', 
            'specialization': 'Joint Replacement',
            'experience_years': 10,
            'bio': 'Expert in knee and hip replacements.'
        }
    )
    print("Done.")

if __name__ == '__main__':
    create_users()
