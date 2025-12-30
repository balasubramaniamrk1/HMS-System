from django.db import models
from django.utils import timezone
from doctors.models import Doctor

class Ward(models.Model):
    WARD_TYPES = [
        ('general', 'General Ward'),
        ('icu', 'ICU'),
        ('private', 'Private Room'),
        ('emergency', 'Emergency'),
    ]
    name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPES)
    floor = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_ward_type_display()})"

class Bed(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, help_text="Daily charge for this bed")
    
    def __str__(self):
        return f"{self.ward.name} - Bed {self.bed_number}"

class Admission(models.Model):
    STATUS_CHOICES = [
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ]
    
    # Linking to string 'appointments.AppointmentRequest' or just Patient Name for simplicity now
    # Ideally link to a Patient model. Using Name/Phone for now as in Appointments.
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20)
    patient_age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M','Male'), ('F','Female'), ('O','Other')], blank=True)
    
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='admissions')
    
    admission_date = models.DateTimeField(default=timezone.now)
    discharge_date = models.DateTimeField(null=True, blank=True)
    discharge_notes = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='admitted')
    
    def __str__(self):
        return f"{self.patient_name} - {self.bed}"
    
    def save(self, *args, **kwargs):
        # Update Bed Status
        if self.pk is None and self.status == 'admitted':
            self.bed.status = 'occupied'
            self.bed.save()
        elif self.status == 'discharged':
            self.bed.status = 'available'
            self.bed.save()
            if not self.discharge_date:
                self.discharge_date = timezone.now()
        super().save(*args, **kwargs)
