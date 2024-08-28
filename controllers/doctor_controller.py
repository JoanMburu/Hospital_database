from flask import jsonify, request
from models import db, Doctor, Patient
from functools import lru_cache

class DoctorController:
    def add_doctor_with_patients(self):
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

    def get_all_doctors(self):
        doctors = Doctor.query.all()
        if not doctors:
            return jsonify({'error': 'No doctors found'}), 404
        return jsonify([{'id': doctor.id, 'name': doctor.name} for doctor in doctors]), 200

    @lru_cache(maxsize=32)
    def get_patients_by_doctor(self, doctor_id):
        patients = Patient.query.filter_by(doctor_id=doctor_id).all()
        if not patients:
            return jsonify({'error': 'No patients found for this doctor'}), 404
        return jsonify([{'id': patient.id, 'name': patient.name} for patient in patients]), 200

    def update_doctor(self, doctor_id):
        data = request.get_json()
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        if 'name' in data:
            doctor.name = data['name']
        
        db.session.commit()
        return jsonify({'message': 'Doctor updated successfully!'}), 200

    def get_cache_info(self):
        cache_info = self.get_patients_by_doctor.cache_info()
        return jsonify({
            'hits': cache_info.hits,
            'misses': cache_info.misses,
            'maxsize': cache_info.maxsize,
            'currsize': cache_info.currsize
        }), 200

