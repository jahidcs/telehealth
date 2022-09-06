from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from account.models import User
from doctor.models import Doctor
from patient.models import Patient


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
        fields = ['id', 'phone', 'role_id']


class PatientProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient', 'pid', 'bg', 'dob', 'district']


class DoctorUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'role_id']


class DoctorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor', 'did', 'bmdc', 'speciality', 'qualification', 'district']
