from django.contrib import admin
from patient.models import Patient, Appointment


class PatientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = Patient.objects.filter().order_by('id')
        return queryset

    list_display = ('patient', 'pid', )
    fieldsets = (
        ('Patient', {'fields': ('patient', 'pid')}),
        ('Identifier', {'fields': ('dob','bg',)}),
        ('others', {'fields': ('district',)}),
    )
    # readonly_fields = ('patient',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'appointment_id', 'schedule_id', 'pat_id', 'appointment_date', 'appointment_status', 'payment_status', 'is_completed')
    list_filter = ('payment_status',)
    fieldsets = (
        ('Patient', {'fields': ('patient_id',)}),
        ('Schedule', {'fields': ('schedule_id', 'doctor_id')}),
        ('Appointment',{'fields': ('pat_id', 'appointment_date', 'appointment_status', 'payment_status', 'is_completed', 'reason', 'doctor_comment')}),
    )


# admin.site.register(Patient, PatientAdmin)
admin.site.register(Patient)
admin.site.register(Appointment, AppointmentAdmin)
