from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.clinic_register_view, name='clinic_register_view'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home_view, name='home_view'),
]


