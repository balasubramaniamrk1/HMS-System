import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User, Group

def assign_front_desk():
    # 1. Create 'Front Desk' Group (and alias Receptionist to it logic-wise if needed, but for now just adding user)
    group_name = 'Front Desk'
    group, _ = Group.objects.get_or_create(name=group_name)
    
    # 2. Get User
    try:
        user = User.objects.get(username='receptionist')
        user.groups.add(group)
        print(f"Added 'receptionist' to '{group_name}'")
    except User.DoesNotExist:
        print("User 'receptionist' not found.")

if __name__ == '__main__':
    assign_front_desk()
