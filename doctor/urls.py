from django.urls import path
from doctor.views import (
    DoctorRegistration,
    DoctorLogin,
    DoctorProfileAccess,
    DoctorScheduleSet,
    AppointmentList
)

urlpatterns = [
    path('register/', DoctorRegistration.as_view(), name='doctor-registration'),
    path('login/', DoctorLogin.as_view(), name='doctor-login'),
    path('profile/', DoctorProfileAccess.as_view(), name='profile'),
    path('schedule/', DoctorScheduleSet.as_view(), name='doctor-schedule'),
    path('appointments/', AppointmentList.as_view(), name='doctor-appointment'),
]
