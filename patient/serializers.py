from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from account.models import User
from doctor.models import Doctor, DoctorSchedule
from patient.models import Patient, Appointment


class PatientPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']


class PatientOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'otp']


class PatientUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'name', 'gender', 'role_id']


class PatientProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient', 'pid', 'bg', 'dob', 'district']


class PatientAppointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient_id', 'pat_id', 'schedule_id', 'appointment_date', 'doctor_id', 'reason', 'appointment_status', 'payment_status', 'doctor_comment', 'is_completed']


class DoctorUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'role_id']


class DoctorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor', 'did', 'bmdc', 'speciality', 'qualification', 'district']


class DoctorScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ['doctor_id', 'did', 'schedule_id', 'schedule_day', 'start_time', 'end_time', 'avg_consulting_time', 'schedule_status']
