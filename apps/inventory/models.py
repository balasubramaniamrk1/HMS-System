from django.db import models
from django.utils import timezone
from datetime import timedelta
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)], help_text="Rating from 1 to 5")
    
    def __str__(self):
        return self.name

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    STATUS_CHOICES = (
        ('new', 'Newly Purchased'),
        ('working', 'Working'),
        ('repair', 'Under Repair'),
        ('retired', 'Retired'),
    )
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_equipment')
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    model_number = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    useful_life = models.PositiveIntegerField(default=5, help_text="Useful life in years for depreciation")
    location = models.CharField(max_length=200, help_text="Department or Room Name")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='working')
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    barcode_data = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Scan barcode from product")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR Code on save if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # QR Content: Name, Serial, URL (placeholder for now)
            qr_data = f"ID:{self.serial_number}\nName:{self.name}\nModel:{self.model_number}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f'qr_{self.serial_number}.png'
            self.qr_code.save(file_name, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class MaintenanceContract(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='amc_records')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    # Keeping provider_name temporarily for backward compatibility if needed, else we can migrate content to Vendor
    provider_name = models.CharField(max_length=200, blank=True, help_text="Legacy field") 
    contract_start = models.DateField()
    contract_end = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    support_contact = models.CharField(max_length=100, help_text="Phone or Email")
    terms = models.TextField(blank=True)

    def is_expiring_soon(self):
        today = timezone.now().date()
        return today <= self.contract_end <= today + timedelta(days=30)
    
    def __str__(self):
        return f"AMC for {self.equipment.name} ({self.contract_end})"

class MaintenanceLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_logs')
    date = models.DateField(default=timezone.now)
    performed_by = models.CharField(max_length=200, help_text="Technician or Vendor Name")
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Log: {self.equipment.name} on {self.date}"

class Consumable(models.Model):
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10, help_text="Alert when stock falls below this")
    unit = models.CharField(max_length=50, help_text="e.g., box, pcs, liters")
    barcode_data = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Scan barcode from product")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity_in_stock <= self.minimum_stock_level

    def __str__(self):
        return self.name
