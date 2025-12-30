import os
import sys
import django
from django.utils import timezone
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from admissions.models import Ward, Bed, Admission
from doctors.models import Doctor

def setup_ipd_data():
    print("Setting up IPD Data...")
    
    # 1. Create Wards
    ward_gen, _ = Ward.objects.get_or_create(
        name="General Ward A",
        defaults={'ward_type': 'general', 'floor': '1st Floor'}
    )
    ward_icu, _ = Ward.objects.get_or_create(
        name="ICU 1",
        defaults={'ward_type': 'icu', 'floor': '2nd Floor'}
    )
    print(f"Wards created: {ward_gen}, {ward_icu}")
    
    # 2. Create Beds
    for i in range(1, 6):
        bed_num = f"G-{i}"
        Bed.objects.get_or_create(
            ward=ward_gen,
            bed_number=bed_num,
            defaults={'price_per_day': Decimal('500.00')}
        )
    
    for i in range(1, 3):
        bed_num = f"ICU-{i}"
        Bed.objects.get_or_create(
            ward=ward_icu,
            bed_number=bed_num,
            defaults={'price_per_day': Decimal('2000.00')}
        )
    print("Beds created.")
    
    # 3. Create Admission
    # Need a doctor
    doctor = Doctor.objects.first()
    if not doctor:
        print("No doctor found. Creating dummy doctor.")
        from django.contrib.auth.models import User
        u, _ = User.objects.get_or_create(username='doc_ipd', defaults={'is_staff': True})
        doctor = Doctor.objects.create(user=u, name="Dr. IPD", specialization="General", phone="111")

    bed_to_occupy = ward_gen.beds.filter(status='available').first()
    if bed_to_occupy:
        adm, created = Admission.objects.get_or_create(
            patient_name="John Doe IPD",
            defaults={
                'patient_phone': '9998887776',
                'ward': ward_gen,
                'bed': bed_to_occupy,
                'doctor': doctor,
                'status': 'admitted'
            }
        )
        if created:
            print(f"Created Admission: {adm}")
        else:
            print(f"Admission already exists: {adm}")
    else:
        print("No beds available for admission test.")

if __name__ == "__main__":
    setup_ipd_data()
