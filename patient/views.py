import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.renderer import UserRenderer
from doctor.models import Doctor, DoctorSchedule
from doctor.serializers import ScheduleListSerializer
from patient.models import Patient, Appointment
from patient.serializers import (
    DoctorUserListSerializer,
    DoctorProfileListSerializer,
    PatientPhoneSerializer,
    PatientOtpSerializer,
    PatientUserViewSerializer,
    PatientProfileViewSerializer,
    DoctorScheduleListSerializer,
    PatientAppointListSerializer
)

def token_generator(user):
    refresh = RefreshToken.for_user(user)

    return{
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

def send_otp(phone, otp):
    pass


class PatientAccessOtp(CreateAPIView):
    serializer_class = PatientPhoneSerializer

    def post(self, request):
        result = {}
        try:
            data = request.data
            if 'phone' not in data or data['phone'] == '':
                return Response(
                    {
                        'errors': " give a Phone number"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            generated_otp = str(random.randint(1000, 9999))
            phone = data['phone']
            user = User.objects.filter(phone=phone).first()

            if user:
                user.otp = generated_otp
                user.save()
                result = {
                    'message': 'OTP sent',
                    'phone': user.phone,
                }
                return Response(
                    result,
                    status=status.HTTP_200_OK
                )
            else:
                user = User()
                user.phone = phone = data['phone']
                user.otp = generated_otp
                user.role_id = 'patient'
                user.save()
                patient = Patient()
                patient.patient = user
                patient.pid = user.id
                patient.save()
                send_otp(user.phone, user.otp)
                result = {
                    'message': 'phone number added and otp sent',
                    'phone': user.phone
                }
                return Response(result, status=status.HTTP_201_CREATED)       

        except Exception as ex:
            return Response(
                {
                    'errors': {str(ex)},
                },
                status=status.HTTP_404_NOT_FOUND
            )
        

class CheckOtp(CreateAPIView):
    serializer_class = PatientOtpSerializer
    permission_classes = []

    def put(self, request):
        result = {}

        try:
            data = request.data

            if 'phone' not in data or data['phone'] == '':
                return Response(
                    {
                        'errors': " give a Phone number"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if 'otp' not in data or data['otp'] == '':
                return Response(
                    {
                        'errors': " give OTP number"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.filter(phone=data['phone']).first()
            if user.otp == data['otp']:
                user.is_active = True
                token = RefreshToken.for_user(user)
                user.otp = ''
                user.save()
                token = token_generator(user)
                return Response(
                    {
                        'token': token,
                        'message': 'access provided',
                    },
                    status=status.HTTP_200_OK
                )
                
            else:
                return Response(
                    {
                        'errors': 'otp did not matched'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as ex:
            return Response(
                {
                    'errors': {str(ex)}
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class PatientProfileAccess(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        result = {}
        serializer = PatientUserViewSerializer(request.user)
        patient = serializer.data
        try:
            patient_profile = Patient.objects.filter(patient=patient['id']).first()
            patient_profile = PatientProfileViewSerializer(patient_profile).data
            result['user'] = patient
            result['profile'] = patient_profile
            return Response(result, status=status.HTTP_200_OK)
        except Exception as ex:
            result['status'] = status.HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)


class AppointmentBooking(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PatientUserViewSerializer(request.user)
        patient = serializer.data
        patient = Patient.objects.filter(patient=patient['id']).first()
        data = request.data

        try:
            appointment = Appointment()
            appointment.patient_id = patient
            appointment.pat_id = patient.pid
            appointment.schedule_id = data['schedule_id']
            appointment.appointment_date = data['appointment_date']
            appointment.doctor_id = data['doctor_id']
            appointment.reason = data['reason']
            appointment.save()

            return Response(
                {
                    "message": "appointment created"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as ex:
            return Response(
                {
                    'errors': {str(ex)}
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class DoctorList(ListAPIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            data = request.data
            doctor = Doctor.objects.filter(district=data['district'], speciality=data['speciality']).all()
            doctor = DoctorProfileListSerializer(doctor, many=True).data
            return Response(
                {
                    "profile": doctor
                },
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            return Response(
                {
                    "errors": {str(ex)}
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class PatientAppointmentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Appointment.objects.all()

        #filters
        patient = self.request.query_params.get('pat_id', None)
        if patient:
            queryset = queryset.filter(pat_id=patient)
        serializer = PatientAppointListSerializer(queryset, many=True)
        return Response(serializer.data)


class DoctorDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None, context={'id':id}):
        result = {}
        doctor = User.objects.filter(id=id).first()
        doctor = DoctorUserListSerializer(doctor).data
        doctor_profile = Doctor.objects.filter(doctor=id).first()
        doctor_profile = DoctorProfileListSerializer(doctor_profile).data

        result['user'] = doctor
        result['profile'] = doctor_profile
        return Response(result, status=status.HTTP_200_OK)


class FindDoctor(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Doctor.objects.all()

        # Filters
        district = self.request.query_params.get('district', None)
        speciality = self.request.query_params.get('speciality', None)
        if district or speciality:
            queryset = queryset.filter(district=district, speciality=speciality)
        serializer = DoctorProfileListSerializer(queryset, many=True)
        return Response(serializer.data)


class DoctorScheduleList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = DoctorSchedule.objects.all()
        
        #filters
        did = self.request.query_params.get('did', None)
        if did:
            queryset = queryset.filter(did=did)
        serializer = DoctorScheduleListSerializer(queryset, many=True)
        return Response(serializer.data)


class DoctorScheduleDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = DoctorSchedule.objects.all()

        #filters
        schedule = self.request.query_params.get('schedule_id', None)
        if schedule:
            queryset = queryset.filter(schedule_id=schedule)
        serializer = DoctorScheduleListSerializer(queryset, many=True)
        return Response(serializer.data)
