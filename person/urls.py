from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastrar_pessoa/', views.create_person_view, name='create_person_view'),
    path('historico_medico/', views.person_detail_view, name='person_detail_view'),
    
]