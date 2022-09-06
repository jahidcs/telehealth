from django.db import models
from account.models import User
from account.strings import DAY_CHOICES

########################
# Custom Model Manager #
########################


class DoctorScheduleManager(models.Manager):

    def create_schedule(self, doctor_id, **extra_fields):
        if not doctor_id:
            raise ValueError('Schedule must create against a doctor')
        
        schedule = self.model(
            doctor_id = self.doctor_id,
            **extra_fields,
        )

        schedule.save()
        return schedule


########################
#    Doctor Models     #
########################


class Doctor(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    did = models.IntegerField(null=True, blank=True)
    nid = models.CharField(max_length=100, null=True, blank=False)
    bmdc = models.CharField(max_length=100, null=True, blank=False)
    qualification = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)


class DoctorSchedule(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='for_doctor')
    schedule_id = models.AutoField(primary_key=True, verbose_name='schedule id')
    schedule_day = models.CharField(max_length=50, null=True, blank=False, choices=DAY_CHOICES, verbose_name='schedule day')
    start_time = models.TimeField(verbose_name='start time', auto_now=False, auto_now_add=False)
    end_time = models.TimeField(verbose_name='end time', auto_now=False, auto_now_add=False)
    avg_consulting_time = models.IntegerField(null=True, blank=False, verbose_name='average consulting time')
    schedule_status = models.BooleanField(default=True)

    # objects = DoctorScheduleManager()



