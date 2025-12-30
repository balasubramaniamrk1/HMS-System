import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User, Group

def setup_roles():
    print("Creating Groups...")
    
    groups = {
        'Doctors': ['dr_ariva', 'dr_saravanan'], # Add other doctor usernames if any
        'Inventory Managers': ['inventory_mgr'],
        'Staff': ['nurse_mary', 'receptionist', 'balasubramaniam'], # General staff access
        'IT Admin': ['admin', 'balasubramaniam']
    }
    
    for group_name, usernames in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group '{group_name}' created.")
        else:
            print(f"Group '{group_name}' already exists.")
            
        for username in usernames:
            try:
                user = User.objects.get(username=username)
                user.groups.add(group)
                print(f"User '{username}' added to group '{group_name}'.")
            except User.DoesNotExist:
                print(f"Warning: User '{username}' not found. Skipping.")

    print("Roles setup complete.")

if __name__ == '__main__':
    setup_roles()
