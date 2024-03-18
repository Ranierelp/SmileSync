from django.urls import path
from . import views

urlpatterns = [
    path('odontograma/', views.odontograma, name='odontograma'),
]

