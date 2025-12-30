import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission

def setup_admin():
    # 1. Create Group
    group_name = 'Hospital Admins'
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Group '{group_name}' created.")
    else:
        print(f"Group '{group_name}' already exists.")

    # 2. Create User
    username = 'hadmin'
    email = 'hadmin@example.com'
    password = 'AdminPass123!'
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = "Hospital"
        user.last_name = "Admin"
        user.save()
        print(f"User '{username}' created.")
    else:
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists.")

    # 3. Add to Group
    user.groups.add(group)
    print(f"User '{username}' added to '{group_name}'.")

    print("\nSetup Complete!")
    print(f"Login with: {username} / {password}")

if __name__ == '__main__':
    setup_admin()
