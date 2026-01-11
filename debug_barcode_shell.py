
from pharmacy.models import Medicine, Batch

print("--- Data Debugging (Shell Mode) ---")
meds = Medicine.objects.all()
print(f"Total Medicines: {meds.count()}")

for med in meds:
    print(f"Medicine: {med.name} (ID: {med.id}), Barcode: '{med.barcode}'")
    batches = Batch.objects.filter(medicine=med)
    if batches.exists():
        for b in batches:
            print(f"  - Batch: {b.batch_number}, Qty: {b.quantity}, Expiry: {b.expiry_date}")
    else:
        print("  - No Batches found.")
