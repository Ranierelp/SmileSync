from django.contrib import admin
from .models import CustomUser, Clinic, Company, Dentist

admin.site.register(CustomUser)
admin.site.register(Clinic)
admin.site.register(Company)
admin.site.register(Dentist)



