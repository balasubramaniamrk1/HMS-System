from django.test import TestCase
from doctors.models import Department, Doctor

class DoctorModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Cardiology", description="Heart stuff")
        self.doctor = Doctor.objects.create(
            name="Dr. Smith",
            department=self.dept,
            qualifications="MBBS",
            specialization="Heart Surgery",
            bio="Great doctor",
            experience_years=10
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.slug, "dr-smith")
        self.assertEqual(self.doctor.department.name, "Cardiology")
        self.assertTrue(Doctor.objects.exists())
