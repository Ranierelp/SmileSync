from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.clinic_register, name='clinic_register'),
    path('login/', views.clinic_login, name='clinic_login'),
]


