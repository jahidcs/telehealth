from django.urls import path
from patient.views import (
    DoctorDetails,
    DoctorList,
    PatientAccessOtp,
    CheckOtp,
    PatientProfileAccess,
    AppointmentBooking,
    FindDoctor,
    DoctorScheduleList,
    PatientAppointmentList,
    DoctorScheduleDetails,
    PatientAppointListByUser,
)

urlpatterns = [
    path('otpaccess/', PatientAccessOtp.as_view(), name='otp-access'),
    path('otpcheck/', CheckOtp.as_view(), name='otp-check'),
    path('profile/', PatientProfileAccess.as_view(), name='profile-view'),
    path('appointment/', AppointmentBooking.as_view(), name='appointment-book'),
    path('doctor-list/', DoctorList.as_view(), name='doctor-list'),
    path('find-doctor/', FindDoctor.as_view(), name='doctor-find'),
    path('doctor-profile/<id>/', DoctorDetails.as_view(), name='doctor-profile'),
    path('doctor-schedule/', DoctorScheduleList.as_view(), name='doctor-schedule'),
    path('doctor-schedule-details/', DoctorScheduleDetails.as_view(), name='schedule-details'),
    path('appointment-list/', PatientAppointmentList.as_view(), name='appointment-list'),
    path('appointment-list-user/', PatientAppointListByUser.as_view(), name='patient-appointment-list')
]
