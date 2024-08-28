import unittest
from app import db
from models import Doctor, Patient, Appointment
from faker import Faker
from datetime import datetime

fake = Faker()

class AppointmentControllerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_add_appointment(self):
        """Test adding a new appointment."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            patient = Patient(name=fake.name(), age=30, doctor=doctor)
            db.session.add(doctor)
            db.session.add(patient)
            db.session.commit()

            appointment_data = {
                "patient_id": patient.id,
                "doctor_id": doctor.id,
                "appointment_date": datetime.now().isoformat(),
                "cost": 100.0
            }
            response = self.client.post('/api/appointments', json=appointment_data)

            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)
            self.assertEqual(response.json['cost'], 100.0)

    def test_delete_appointment(self):
        """Test deleting an appointment."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            patient = Patient(name=fake.name(), age=30, doctor=doctor)
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_date=datetime.now(),
                cost=100.0
            )
            db.session.add(doctor)
            db.session.add(patient)
            db.session.add(appointment)
            db.session.commit()

            response = self.client.delete(f'/api/appointments/{appointment.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Appointment deleted successfully!')

if __name__ == '__main__':
    unittest.main()
