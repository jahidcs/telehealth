from datetime import date
from django.db import models
from account.models import User
from account.strings import BLOOD_GROUP_CHOICES

class Patient(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    bg = models.CharField(max_length=4, null=True, blank=True, choices=BLOOD_GROUP_CHOICES)
    district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.patient)


class Appointment(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_id = models.AutoField(primary_key=True)
    pat_id = models.IntegerField(null=True, blank=True)
    schedule_id = models.IntegerField(null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)
    doctor_id = models.IntegerField()
    serial = models.IntegerField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    appointment_status = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)
    doctor_comment = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
