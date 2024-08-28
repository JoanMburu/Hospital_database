from flask import Blueprint
from controllers.doctor_controller import DoctorController
from controllers.patient_controller import PatientController
from controllers.appointment_controller import AppointmentController

bp = Blueprint('controllers', __name__)

doctor_controller = DoctorController()
patient_controller = PatientController()
appointment_controller = AppointmentController()

bp.add_url_rule('/doctors', view_func=doctor_controller.add_doctor_with_patients, methods=['POST'])
bp.add_url_rule('/doctors', view_func=doctor_controller.get_all_doctors, methods=['GET'])
bp.add_url_rule('/doctors/<string:doctor_id>/patients', view_func=doctor_controller.get_patients_by_doctor, methods=['GET'])
bp.add_url_rule('/doctors/<string:doctor_id>', view_func=doctor_controller.update_doctor, methods=['PATCH'])
bp.add_url_rule('/doctors/cache_info', view_func=doctor_controller.get_cache_info, methods=['GET'])

bp.add_url_rule('/patients', view_func=patient_controller.add_patient, methods=['POST'])
bp.add_url_rule('/patients/<string:patient_id>', view_func=patient_controller.get_patient, methods=['GET'])
bp.add_url_rule('/patients/<string:patient_id>', view_func=patient_controller.delete_patient, methods=['DELETE'])
bp.add_url_rule('/patients/<string:patient_id>', view_func=patient_controller.update_patient, methods=['PATCH'])

bp.add_url_rule('/appointments', view_func=AppointmentController().add_appointment, methods=['POST'])
bp.add_url_rule('/appointments/<string:appointment_id>', view_func=AppointmentController().delete_appointment, methods=['DELETE'])