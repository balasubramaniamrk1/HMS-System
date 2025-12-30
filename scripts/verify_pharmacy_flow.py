import os
import django
import json
from django.utils import timezone
from decimal import Decimal

import sys
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User
from doctors.models import Doctor, Department
from appointments.models import AppointmentRequest, Consultation, PrescriptionItem
from pharmacy.models import Medicine, Batch, Sale, SaleItem, MedicineCategory
from billing.models import Invoice

def verify_pharmacy_flow():
    print("--- Starting Verification ---")
    
    # 1. Setup Data
    print("1. Setting up Master Data...")
    user, created = User.objects.get_or_create(username='test_doctor')
    if created:
        user.set_password('password123')
        user.save()
        print("   Created User 'test_doctor' with password 'password123'")
    
    dept, _ = Department.objects.get_or_create(name='General Medicine')
    doctor, _ = Doctor.objects.get_or_create(user=user, defaults={'name': 'Dr. Test', 'department': dept})
    
    cat, _ = MedicineCategory.objects.get_or_create(name='Antibiotics')
    med, _ = Medicine.objects.get_or_create(name='TestMeds 500mg', defaults={'category': cat, 'dosage_form': 'Tablet'})
    
    # Clean up old batches for test
    Batch.objects.filter(medicine=med).delete()
    
    batch = Batch.objects.create(
        medicine=med,
        batch_number='B123',
        expiry_date=timezone.now().date() + timezone.timedelta(days=365),
        quantity=100,
        buy_price=5.0,
        sell_price=10.0
    )
    print(f"   Created Batch {batch.batch_number} with Qty {batch.quantity}")

    # 2. Create Consultation
    print("2. Creating Consultation with Prescription...")
    appt = AppointmentRequest.objects.create(
        name='Test Patient',
        phone='1234567890',
        doctor=doctor,
        preferred_date=timezone.now().date(),
        status='confirmed'
    )
    
    cons = Consultation.objects.create(
        appointment=appt,
        diagnosis='Fever',
        doctor_notes='Rest',
        pharmacy_status='pending'
    )
    
    PrescriptionItem.objects.create(
        consultation=cons,
        medicine_name='TestMeds 500mg',
        dosage='1-0-1',
        duration='5 days'
    )
    print(f"   Created Consultation {cons.id} for {appt.name}")

    # 3. Verify Dashboard Query
    print("3. Verifying Dashboard Query...")
    pending = Consultation.objects.filter(pharmacy_status='pending', prescription_items__isnull=False).distinct()
    if cons in pending:
        print("   ✅ Consultation found in Pending List")
    else:
        print("   ❌ Consultation NOT found in Pending List")

    # 4. Simulate POS Sale (Manual Logic Execution)
    print("4. Simulating POS Sale Execution...")
    
    qty_to_buy = 10
    total_expected = qty_to_buy * batch.sell_price
    
    # Create Invoice
    invoice = Invoice.objects.create(
        patient_name=appt.name,
        doctor=doctor,
        consultation=cons,
        source='pharmacy',
        status='pending',
        total_amount=0
    )
    
    # Create Sale
    sale = Sale.objects.create(
        patient_name=appt.name,
        doctor=doctor,
        consultation=cons,
        invoice=invoice,
        status='completed'
    )
    
    # Deduct Stock (Handled by SaleItem model signal/save method)
    batch.refresh_from_db()
    initial_qty = batch.quantity
    
    SaleItem.objects.create(sale=sale, batch=batch, quantity=qty_to_buy, price_at_sale=batch.sell_price)
    
    invoice.total_amount = total_expected
    invoice.save()
    
    cons.pharmacy_status = 'dispensed'
    cons.save()
    
    # 5. Verify Results
    print("5. Verifying Results...")
    
    batch.refresh_from_db()
    print(f"   Stock: Initial {initial_qty} -> Now {batch.quantity}")
    if batch.quantity == (initial_qty - qty_to_buy):
        print("   ✅ Stock Deducted Correctly")
    else:
        print(f"   ❌ Stock Deduction Failed! Expected {initial_qty - qty_to_buy}, got {batch.quantity}")
        
    cons.refresh_from_db()
    print(f"   Consultation Status: {cons.pharmacy_status}")
    if cons.pharmacy_status == 'dispensed':
         print("   ✅ Status Updated Correctly")
    else:
         print("   ❌ Status Update Failed")
         
    inv = Invoice.objects.get(id=invoice.id)
    print(f"   Invoice Total: {inv.total_amount}")
    if inv.total_amount == total_expected:
        print("   ✅ Invoice Total Correct")
    else:
        print("   ❌ Invoice Total Incorrect")

if __name__ == '__main__':
    verify_pharmacy_flow()
