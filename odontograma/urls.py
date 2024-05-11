from django.urls import path
from . import views

urlpatterns = [
    path('odontograma/', views.odontograma_view, name='odontograma_view'),
]

