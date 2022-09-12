from email.policy import default
from rest_framework import serializers
from doctor.models import Doctor, DoctorSchedule
from account.models import User
from patient.models import Appointment


class DoctorRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type':'password'},
        write_only=True
    )
    role_id = serializers.CharField(default="doctor")

    class Meta:
        model = User
        fields = [
            'name', 'gender', 'role_id', 
            'email', 'phone', 
            'password', 'password2',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password does't matched")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class DoctorLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class DoctorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields =['doctor','did', 'nid', 'bmdc', 'qualification', 'speciality', 'district']


class DoctorUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'gender', 'role_id', 'id']


class DoctorScheduleSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(source='doctor.id')
    class Meta:
        model = DoctorSchedule
        fields = [
            'doctor_id', 'did', 'schedule_id',  'schedule_status',
            'schedule_day', 'start_time', 'end_time', 
            'avg_consulting_time'
        ]

        def create(self, validate_data):
            return DoctorSchedule.objects.create_schedule(**validate_data)


class AppointmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient_id', 'pat_id', 'appointment_id', 'schedule_id', 'doctor_id', 'serial', 'appointment_date', 'reason', 'appointment_status', 'payment_status', 'doctor_comment', 'is_completed']


class ScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ['doctor_id', 'did', 'schedule_id',  'schedule_status',
            'schedule_day', 'start_time', 'end_time', 
            'avg_consulting_time']