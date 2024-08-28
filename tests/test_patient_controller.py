import unittest
from app import app, db
from models import Patient, Doctor
from faker import Faker
import json

fake = Faker()

class PatientControllerTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize a new database for each test."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_patient(self):
        """Test adding a new patient."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()

        patient_data = {"name": fake.name(), "doctor_id": doctor.id}
        response = self.client.post('/patients', data=json.dumps(patient_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Patient added successfully!', response.get_json().get('message'))

    def test_get_patient(self):
        """Test retrieving a patient by ID."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()
            patient = Patient(name=fake.name(), doctor_id=doctor.id)
            db.session.add(patient)
            db.session.commit()
            patient_id = patient.id

        response = self.client.get(f'/patients/{patient_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], patient_id)

    def test_delete_patient(self):
        """Test deleting a patient."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()
            patient = Patient(name=fake.name(), doctor_id=doctor.id)
            db.session.add(patient)
            db.session.commit()
            patient_id = patient.id

        response = self.client.delete(f'/patients/{patient_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Patient deleted successfully!', response.get_json().get('message'))

    def test_update_patient(self):
        """Test updating a patient's information."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()
            patient = Patient(name=fake.name(), doctor_id=doctor.id)
            db.session.add(patient)
            db.session.commit()
            patient_id = patient.id

        update_data = {"name": "Updated Patient Name"}
        response = self.client.patch(f'/patients/{patient_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Patient updated successfully!', response.get_json().get('message'))

