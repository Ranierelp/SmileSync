from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.clinic_register_view, name='clinic_register_view'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home_view, name='home_view'),
    path('cadastro_dentista/', views.create_dentist_view, name='create_dentist_view'),
    path('cadastro_empresa/', views.create_company_view, name='create_company_view'),
    path('lista_dentistas/', views.list_dentists_view, name='list_dentists_view'),
    path('lista_empresas/', views.list_companies_view, name='list_companies_view'),
    path('logout/', views.logout_view, name='logout'),
    path('deletar_dentista/<str:pk>/', views.delete_dentist_view, name='delete_dentist_view'),
    path('deletar_empresa/<str:pk>/', views.delete_company_view, name='delete_company_view'),
    path('planos/', views.planos_view, name='planos_view'),
    path('perfil/', views.profile_view, name='profile_view'),
 

]


