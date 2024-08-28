from faker import Faker
from models import db, Doctor, Patient
import uuid

fake = Faker()

def seed_data():
    for _ in range(10):
        doctor = Doctor(id=str(uuid.uuid4()), name=fake.name())
        db.session.add(doctor)
        db.session.commit()
        
        for _ in range(5):
            patient = Patient(id=str(uuid.uuid4()), name=fake.name(), doctor_id=doctor.id)
            db.session.add(patient)
        
        db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()
        seed_data()
