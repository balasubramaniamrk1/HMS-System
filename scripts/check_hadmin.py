import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User

def check_hadmin():
    try:
        user = User.objects.get(username='hadmin')
        print(f"User found: {user.username}")
        print(f"Groups: {[g.name for g in user.groups.all()]}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Active: {user.is_active}")
        print(f"Has Staff Profile: {hasattr(user, 'staff_profile')}")
    except User.DoesNotExist:
        print("User 'hadmin' NOT found.")

if __name__ == "__main__":
    check_hadmin()
