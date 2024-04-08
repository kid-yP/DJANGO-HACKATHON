from django.contrib import admin
from .models import CustomUser,Client,Tutor
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('full_name', 'email', 'role')

class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name','get_email','get_role']

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    def get_role(self, obj):
        return obj.user.role
    get_role.short_description = 'Role'



class TutorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'get_role']

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    def get_role(self, obj):
        return obj.user.role
    get_role.short_description = 'Role'

admin.site.register(Client, ClientAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

