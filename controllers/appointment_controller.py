from flask import Blueprint, jsonify, request
from models import db, Appointment, Patient, Doctor
from datetime import datetime

bp = Blueprint('appointment_controller', __name__)

class AppointmentController:
    def add_appointment(self):
        data = request.get_json()
        if 'patient_id' not in data or 'doctor_id' not in data or 'appointment_date' not in data or 'cost' not in data:
            return jsonify({'error': 'Missing required fields'}), 422

        patient = Patient.query.get(data['patient_id'])
        doctor = Doctor.query.get(data['doctor_id'])

        if not patient or not doctor:
            return jsonify({'error': 'Patient or Doctor not found'}), 404

        try:
            appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid date format, should be YYYY-MM-DD HH:MM:SS'}), 422

        new_appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            cost=data['cost']
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
            'id': new_appointment.id,
            'patient_id': new_appointment.patient_id,
            'doctor_id': new_appointment.doctor_id,
            'appointment_date': new_appointment.appointment_date.isoformat(),
            'cost': new_appointment.cost
        }), 201

    def delete_appointment(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully!'}), 200
