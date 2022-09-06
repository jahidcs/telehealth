from unittest import result
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from doctor.models import Doctor, DoctorSchedule
from patient.models import Appointment
from account.models import User
from account.renderer import UserRenderer
from doctor.serializers import (
    AppointmentListSerializer,
    DoctorSerializer,
    DoctorRegisterSerializer,
    DoctorLoginSerializer,
    DoctorUserViewSerializer,
    DoctorScheduleSerializer,
)

def token_generator(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class DoctorRegistration(CreateAPIView):
    permission_classes = []
    
    def post(self, request):
        try:
            data = request.data

            if 'name' not in data or data['name'] == '':
                return Response(
                    {
                        'errors': 'Name should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'email' not in data or data['email'] == '':
                return Response(
                    {
                        'errors': 'Email should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'phone' not in data or data['phone'] == '':
                return Response(
                    {
                        'errors': 'Phone number should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'role_id' not in data or data['role_id'] == '':
                return Response(
                    {
                        'errors': 'Role should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'password' not in data or data['password'] == '':
                return Response(
                    {
                        'errors': 'Password should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'password2' not in data or data['password2'] == '':
                return Response(
                    {
                        'errors': 'Confirm your password. It is mandatory'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'nid' not in data or data['nid'] == '':
                return Response(
                    {
                        'errors': 'NID number should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'bmdc' not in data or data['bmdc'] == '':
                return Response(
                    {
                        'errors': 'BMDC number should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'qualification' not in data or data['qualification'] == '':
                return Response(
                    {
                        'errors': 'Qualification should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'speciality' not in data or data['speciality'] == '':
                return Response(
                    {
                        'errors': 'Speciality should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'district' not in data or data['district'] == '':
                return Response(
                    {
                        'errors': 'district should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if data['password'] != data['password2']:
                return Response(
                    {
                        "errors": "Password and confirm password does't matched"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(email=['email']).first()

            if user:
                return Response(
                    {
                        'errors': 'You already registered'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not user:
                user = User()
                user.name = data['name']
                user.email = data['email']
                user.phone = data['phone']
                user.gender = data['gender']
                user.role_id = data['role_id']
                user.password = make_password(data['password'])
                user.save()
                print(user)
                doctor = Doctor()
                doctor.doctor = user
                doctor.did = user.id
                doctor.nid = data['nid']
                doctor.bmdc = data['bmdc']
                doctor.qualification = data['qualification']
                doctor.speciality = data['speciality']
                doctor.district = data['district']
                doctor.save()
                result = {
                    'status': status.HTTP_201_CREATED,
                    'message': 'Registration Successfull'
                }
                return Response(result, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(
                {
                    'errors': {str(ex)}
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DoctorRegistrationV2(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        doctor = Doctor()
        serializer = DoctorRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = token_generator(user)
            return Response(
                {
                    'token': token,
                    'message': 'Registration Successful'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DoctorInfo(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        pass


class DoctorLogin(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = DoctorLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print("serializer: ", serializer.data)
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            doctor = authenticate(email=email, password=password)

            if doctor is not None:
                token = token_generator(doctor)
                return Response(
                    {
                        'token': token,
                        'message': 'Login Successfull'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'errors':{
                            'non_field_errors':['Email or password is not valid']
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DoctorProfileAccess(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        result = {}
        serializer = DoctorUserViewSerializer(request.user)
        doctor = serializer.data
        try:
            doctor_profile = Doctor.objects.filter(doctor=doctor['id']).first()
            doctor_profile = DoctorSerializer(doctor_profile).data
            result['user'] = doctor
            result['profile'] = doctor_profile
            return Response(result, status=status.HTTP_200_OK)
        except Exception as ex:
            result['status'] = status.HTTP_400_BAD_REQUEST
            result['message'] = str(ex)
            return Response(result)


class DoctorScheduleSet(CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = DoctorUserViewSerializer(request.user)
        doctor = serializer.data
        doctor = Doctor.objects.filter(doctor=doctor['id']).first()   
        data = request.data
        if 'schedule_day' not in data or data['schedule_day'] == '':
                return Response(
                    {
                        'errors': 'schedule_day should be provided'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        if 'start_time' not in data or data['start_time'] == '':
            return Response(
                {
                    'errors': 'start_time should be provided'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'end_time' not in data or data['end_time'] == '':
            return Response(
                {
                    'errors': 'end_time should be provided'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'avg_consulting_time' not in data or data['avg_consulting_time'] == '':
            return Response(
                {
                    'errors': 'avg_consulting_time should be provided'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor_schedule = DoctorSchedule()
            doctor_schedule.doctor_id = doctor
            doctor_schedule.schedule_day = data['schedule_day']
            doctor_schedule.start_time = data['start_time']
            doctor_schedule.end_time = data['end_time']
            doctor_schedule.avg_consulting_time = data['avg_consulting_time']
            doctor_schedule.save()

            return Response(
                {
                    "message": "schedule created"
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
        

class AppointmentList(ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        result = {}
        doctor = DoctorUserViewSerializer(request.user).data
        appointment = Appointment.objects.filter(doctor_id=doctor['id']).all()
        print(appointment)
        appointment = AppointmentListSerializer(appointment, many=True).data

        result['appointment_list'] = appointment
        return Response(result, status=status.HTTP_200_OK)
