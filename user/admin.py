from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Clinic, Dentist, Company

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'phone', 'is_staff', 'is_active', 'deleted_at', 'updated_at', 'created_at')    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'phone', )}),
        ('Permissões', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('__str__','user', 'cnpj')
    
@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'cro', 'clinic')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('__str__','user', 'cnpj', 'clinic', 'address')
