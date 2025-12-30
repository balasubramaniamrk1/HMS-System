import os
import sys
import django
from datetime import date, timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from inventory.models import Vendor, EquipmentCategory, Equipment, MaintenanceContract, Consumable

def setup_inventory_test():
    # 1. Create 'Inventory Managers' Group and User
    group, _ = Group.objects.get_or_create(name='Inventory Managers')
    
    username = 'item_mgr'
    password = 'password123'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.email = 'inventory@healthplus.com'
        user.save()
        print(f"Created user '{username}'")
    
    user.groups.add(group)
    print(f"Added '{username}' to 'Inventory Managers'")

    # 2. Create Vendor
    vendor, _ = Vendor.objects.get_or_create(
        name="MedTech Supplies Inc.",
        defaults={'phone': '555-0123', 'email': 'sales@medtech.com'}
    )

    # 3. Create Category
    category, _ = EquipmentCategory.objects.get_or_create(name="Diagnostic Imaging")

    # 4. Create Equipment
    equipment, _ = Equipment.objects.get_or_create(
        serial_number="XR-2025-001",
        defaults={
            'name': "X-Ray Machine Model X",
            'category': category,
            'vendor': vendor,
            'cost': 50000.00,
            'purchase_date': date.today() - timedelta(days=365),
            'location': 'Radiology Room 1'
        }
    )

    # 5. Create Expiring AMC (Ends in 10 days)
    amc_end = date.today() + timedelta(days=10)
    MaintenanceContract.objects.get_or_create(
        equipment=equipment,
        contract_end=amc_end,
        defaults={
            'vendor': vendor,
            'provider_name': vendor.name,
            'contract_start': date.today() - timedelta(days=355),
            'cost': 2000.00,
            'support_contact': 'support@medtech.com'
        }
    )
    print(f"Created AMC expiring on {amc_end}")

    # 6. Create Low Stock Consumable
    Consumable.objects.get_or_create(
        name="X-Ray Film",
        defaults={
            'quantity_in_stock': 5, # Below default min of 10
            'minimum_stock_level': 20,
            'unit': 'sheets',
            'vendor': vendor
        }
    )
    print("Created Low Stock Consumable: X-Ray Film (5 sheets)")

if __name__ == '__main__':
    setup_inventory_test()
