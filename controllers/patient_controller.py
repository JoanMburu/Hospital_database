from flask import jsonify, request
from models import db, Patient

class PatientController:
    def add_patient(self):
        data = request.get_json()
        if 'name' not in data or 'doctor_id' not in data:
            return jsonify({'error': 'Invalid data format'}), 422

        new_patient = Patient(name=data['name'], doctor_id=data['doctor_id'])
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({'message': 'Patient added successfully!'}), 200

    def get_patient(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify({'id': patient.id, 'name': patient.name, 'doctor_id': patient.doctor_id}), 200

    def delete_patient(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted successfully!'}), 200

    def update_patient(self, patient_id):
        data = request.get_json()
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        if 'name' in data:
            patient.name = data['name']
        if 'doctor_id' in data:
            patient.doctor_id = data['doctor_id']
        
        db.session.commit()
        return jsonify({'message': 'Patient updated successfully!'}), 200


