import os
import django
import sys

# Setup Django environment
sys.path.append('/Users/balasubramaniam/Desktop/HMS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

# Import models AFTER setup
from apps.pharmacy.models import Medicine, Batch

print("--- Data Debugging ---")
meds = Medicine.objects.all()
print(f"Total Medicines: {meds.count()}")

for med in meds:
    print(f"Medicine: {med.name}, Barcode: '{med.barcode}'")
    batches = Batch.objects.filter(medicine=med)
    if batches.exists():
        for b in batches:
            print(f"  - Batch: {b.batch_number}, Qty: {b.quantity}, Expiry: {b.expiry_date}")
    else:
        print("  - No Batches found.")
