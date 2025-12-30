import os
import django
import sys

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from doctors.models import Doctor

def link_doctors():
    print("Linking Doctors to Users...")
    
    # Mapping: Username -> Doctor Name (partial match or slug)
    mapping = {
        'dr_ariva': 'arivalagan', 
        'dr_saravanan': 'saravanan'
    }

    for username, doc_name_part in mapping.items():
        try:
            user = User.objects.get(username=username)
            # Find doctor by name containing the part
            doctor = Doctor.objects.filter(name__icontains=doc_name_part).first()
            
            if doctor:
                doctor.user = user
                doctor.save()
                print(f"Linked User '{username}' to Doctor '{doctor.name}'.")
            else:
                print(f"Doctor matching '{doc_name_part}' not found for user '{username}'.")
                
        except User.DoesNotExist:
            print(f"User '{username}' not found.")
        except Exception as e:
            print(f"Error linking {username}: {str(e)}")

    print("Done.")

if __name__ == '__main__':
    link_doctors()
