
import django
import os
import sys

sys.path.append('/Users/balasubramaniam/Desktop/HMS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from pharmacy.models import Batch, Medicine
from django.utils import timezone
from django.db.models import Q

print(f"Today: {timezone.now().date()}")

terms = ["AVN", "123456"]

for term in terms:
    print(f"\nSearching for term: '{term}'")
    matches = Batch.objects.filter(
        quantity__gt=0, 
        expiry_date__gte=timezone.now().date()
    ).filter(
        Q(medicine__name__icontains=term) | 
        Q(medicine__barcode__iexact=term) |
        Q(medicine__generic_name__icontains=term)
    ).select_related('medicine').order_by('expiry_date')[:20]
    
    print(f"Found {matches.count()} matches:")
    for b in matches:
        print(f" - {b.medicine.name} (Batch: {b.batch_number}, Qty: {b.quantity}, Exp: {b.expiry_date})")
        is_barcode = (b.medicine.barcode and b.medicine.barcode.lower() == term.lower())
        print(f"   is_barcode: {is_barcode}")
