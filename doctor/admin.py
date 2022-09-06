from django.contrib import admin
from doctor.models import Doctor, DoctorSchedule

# Register your models here.

class DoctorAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = Doctor.objects.filter().order_by('id')
        return queryset

    list_display = ('doctor','did', 'bmdc', 'nid', 'speciality', 'district')
    list_filter = ('speciality',)
    fieldsets = (
        ('Doctor', {'fields': ('doctor', 'did')}),
        ('Identifier', {'fields': ('nid','bmdc',)}),
        ('Professional', {'fields': ('speciality', 'qualification')}),
    )
    readonly_fields = ['did', 'doctor']


class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'schedule_id', 'schedule_day', 'start_time', 'end_time', 'avg_consulting_time', 'schedule_status')
    list_filter = ('schedule_day',)
    fieldsets = (
        ('Doctor', {'fields': ('doctor_id',)}),
        ('Identifier', {'fields': ('schedule_day', 'schedule_status',)}),
        ('Schedule details', {'fields': ('start_time', 'end_time', 'avg_consulting_time',)}),
    )


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorSchedule, DoctorScheduleAdmin)


