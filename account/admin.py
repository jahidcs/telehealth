from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'phone', 'name', 'is_active', 'is_admin', 'role_id', 'otp')
    list_filter = ('is_admin', 'role_id',)

    fieldsets = (
        ('User Credentials', {'fields': ('email', 'phone', 'password', 'otp')}),
        ('Personal info', {'fields': ('name', 'gender', 'role_id')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'gender', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('role_id', 'id')
    filter_horizontal = ()


admin.site.register(User, UserModelAdmin)
