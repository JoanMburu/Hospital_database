from flask import Blueprint, jsonify, request
from models import db, Doctor, Patient
from functools import lru_cache

bp = Blueprint('controllers', __name__)

from flask import Blueprint, jsonify, request
from models import db, Doctor, Patient

bp = Blueprint('controllers', __name__)

@bp.route('/doctors', methods=['POST'])
def add_doctor_with_patients():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Invalid data format. Expected a list of doctors.'}), 422
    
    for doctor_data in data:
        if 'name' not in doctor_data or 'patients' not in doctor_data:
            return jsonify({'error': 'Missing required fields: name or patients.'}), 404
        
        if not isinstance(doctor_data['patients'], list):
            return jsonify({'error': 'Invalid format for patients. Expected a list.'}), 422

        new_doctor = Doctor(name=doctor_data['name'])
        db.session.add(new_doctor)
        db.session.commit()

        for patient_data in doctor_data['patients']:
            if 'name' not in patient_data:
                return jsonify({'error': 'Missing required field: name in patients.'}), 404
            
            new_patient = Patient(name=patient_data['name'], doctor_id=new_doctor.id)
            db.session.add(new_patient)

        db.session.commit()
    
    return jsonify({'message': 'Doctor and patients added successfully!'}), 200


@bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    if 'name' not in data or 'doctor_id' not in data:
        return jsonify({'error': 'Invalid data format'}), 422

    new_patient = Patient(name=data['name'], doctor_id=data['doctor_id'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully!'}), 200

@bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    doctors = Doctor.query.all()
    if not doctors:
        return jsonify({'error': 'No doctors found'}), 404
    return jsonify([{'id': doctor.id, 'name': doctor.name} for doctor in doctors]), 200

@bp.route('/doctors/<int:doctor_id>/patients', methods=['GET'])
@lru_cache(maxsize=32)
def get_patients_by_doctor(doctor_id):
    patients = Patient.query.filter_by(doctor_id=doctor_id).all()
    if not patients:
        return jsonify({'error': 'No patients found for this doctor'}), 404
    return jsonify([{'id': patient.id, 'name': patient.name} for patient in patients]), 200

@bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify({'id': patient.id, 'name': patient.name, 'doctor_id': patient.doctor_id}), 200

@bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully!'}), 200
