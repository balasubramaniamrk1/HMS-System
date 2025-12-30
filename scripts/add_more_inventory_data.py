import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from inventory.models import Vendor, EquipmentCategory, Equipment, MaintenanceContract, Consumable

def add_more_data():
    vendor = Vendor.objects.first() # Reuse existing vendor
    category = EquipmentCategory.objects.first()

    # 1. Add another Low Stock Consumable
    Consumable.objects.get_or_create(
        name="Syringes (5ml)",
        defaults={
            'quantity_in_stock': 50,
            'minimum_stock_level': 100, # Threshold triggers here
            'unit': 'units',
            'vendor': vendor
        }
    )
    print("Added Low Stock Item: Syringes (50/100)")

    # 2. Add another Expiring AMC (Due in 20 days)
    # First create equipment
    equip, _ = Equipment.objects.get_or_create(
        serial_number="CT-SCAN-002",
        defaults={
            'name': "CT Scanner Advanced",
            'category': category,
            'vendor': vendor,
            'location': 'Radiology Room 2',
            'cost': 150000.00
        }
    )

    # Then create AMC
    amc_end = date.today() + timedelta(days=20)
    MaintenanceContract.objects.get_or_create(
        equipment=equip,
        contract_end=amc_end,
        defaults={
            'vendor': vendor,
            'provider_name': vendor.name,
            'contract_start': date.today() - timedelta(days=345),
            'cost': 5000.00,
            'support_contact': 'support@medtech.com'
        }
    )
    print(f"Added Expiring AMC for CT Scanner (Due: {amc_end})")

if __name__ == '__main__':
    add_more_data()
