import os
import sys
import django

# Set up path so 'apps' can be found
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps')) 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.utils_logging import log_admin_action

def verify_logging():
    try:
        user = User.objects.get(username='hadmin')
        log_admin_action(user, "TEST_ACTION", "Verifying log system")
        
        log_file = os.path.join(BASE_DIR, 'logs', 'hms_audit.log')
        if os.path.exists(log_file):
            print(f"Log file found at: {log_file}")
            with open(log_file, 'r') as f:
                lines = f.readlines()
                print(f"Last log entry: {lines[-1].strip()}")
        else:
            print("Log file NOT found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_logging()
