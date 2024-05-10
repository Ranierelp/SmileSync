from django.core.exceptions import ValidationError
from .models import Person

def cpf_unique(value:str):
    if Person.objects.filter(cpf=value).exists():
        raise ValidationError('Este CPF já está em uso. Por favor, insira outro válido.')