from django.urls import path
from . import views

urlpatterns = [
    path('odontograma/<str:cpf>', views.odontograma_view, name='odontograma_view'),
]

