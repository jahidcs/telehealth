from django.urls import path
from patient.views import (
    DoctorDetails,
    DoctorList,
    PatientAccessOtp,
    CheckOtp,
    PatientProfileAccess,
    AppointmentBooking,
)

urlpatterns = [
    path('otpaccess/', PatientAccessOtp.as_view(), name='otp-access'),
    path('otpcheck/', CheckOtp.as_view(), name='otp-check'),
    path('profile/', PatientProfileAccess.as_view(), name='profile-view'),
    path('appointment/', AppointmentBooking.as_view(), name='appointment-book'),
    path('doctor-list/', DoctorList.as_view(), name='doctor-list'),
    path('doctor-profile/<id>/', DoctorDetails.as_view(), name='doctor-profile')
]
