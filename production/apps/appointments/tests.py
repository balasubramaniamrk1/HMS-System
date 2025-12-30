from django.test import TestCase
from django.utils import timezone
from .models import AppointmentRequest, Consultation

class ConsultationWorkflowTest(TestCase):
    def test_full_workflow(self):
        # 1. Create Appointment
        appt = AppointmentRequest.objects.create(
            name="John Doe", phone="1234567890",
            preferred_date=timezone.now().date(),
            preferred_time="10:00 AM",
            status='pending'
        )
        self.assertEqual(appt.status, 'pending')

        # 2. Staff Confirms
        appt.status = 'confirmed'
        appt.save()
        self.assertEqual(appt.status, 'confirmed')

        # 3. Doctor Consults
        consult = Consultation.objects.create(
            appointment=appt,
            diagnosis="Flu",
            prescription="Paracetamol"
        )
        self.assertEqual(consult.appointment, appt)

        # 4. Mark Completed (simulated view logic)
        appt.status = 'completed'
        appt.save()
        
        self.assertEqual(appt.status, 'completed')
        self.assertEqual(appt.consultation.diagnosis, "Flu")
