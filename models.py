import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class Doctor(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=True) 
    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.String(36), db.ForeignKey('doctor.id'), nullable=False)

class Appointment(db.Model):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey('patient.id'), nullable=False)
    doctor_id = Column(String(36), ForeignKey('doctor.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    cost = Column(Float, nullable=False)
    patient = relationship('Patient', backref='appointments')
    doctor = relationship('Doctor', backref='appointments')
