import unittest
from app import app, db
from models import Doctor, Patient
from faker import Faker
import json

fake = Faker()

class DoctorControllerTestCase(unittest.TestCase):

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

    def test_add_doctor_with_patients(self):
        """Test adding a doctor with patients."""
        doctor_data = [
            {
                "name": fake.name(),
                "patients": [{"name": fake.name()} for _ in range(3)]
            }
        ]
        response = self.client.post('/doctors', data=json.dumps(doctor_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Doctor and patients added successfully!', response.get_json().get('message'))

    def test_get_all_doctors(self):
        """Test retrieving all doctors."""
        # Seed some doctors
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()

        response = self.client.get('/doctors')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_patients_by_doctor(self):
        """Test retrieving patients by doctor ID."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()
            doctor_id = doctor.id
            # Add some patients
            patients = [Patient(name=fake.name(), doctor_id=doctor_id) for _ in range(2)]
            db.session.add_all(patients)
            db.session.commit()

        response = self.client.get(f'/doctors/{doctor_id}/patients')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_doctor(self):
        """Test updating a doctor's information."""
        with self.app.app_context():
            doctor = Doctor(name=fake.name())
            db.session.add(doctor)
            db.session.commit()
            doctor_id = doctor.id

        update_data = {"name": "Updated Doctor Name"}
        response = self.client.patch(f'/doctors/{doctor_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Doctor updated successfully!', response.get_json().get('message'))

    def test_get_cache_info(self):
        """Test retrieving cache information."""
        response = self.client.get('/doctors/cache_info')
        self.assertEqual(response.status_code, 200)
        self.assertIn('hits', response.get_json())

