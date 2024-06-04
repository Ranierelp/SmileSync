from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastrar_pessoa/', views.create_person_view, name='create_person_view'),
    path('prontuario_eletronico/', views.person_detail_view, name='person_detail_view'),
    path('prontuario_eletronico/<str:cpf>/', views.person_create_medical_record_view, name='person_create_medical_record_view'),
    path('listar_pessoas/', views.list_person_view, name='list_person_view'),
    
]