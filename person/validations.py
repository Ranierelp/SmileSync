from django.core.exceptions import ValidationError
from .models import Person

def cpf_unique(value:str):
    if Person.objects.filter(cpf=value).exists():
        raise ValidationError('Este CPF já está em uso. Por favor, insira outro válido.')
    
def remove_cpf_formatting(cpf:str):
    cpf_unformatted = cpf.replace(".", "").replace("-", "")
    return cpf_unformatted
def person_email_unique(value:str) :
    if Person.objects.filter(email=value).exists():
        raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

def person_phone_unique(value:str):
    if Person.objects.filter(phone=value).exists():
        raise ValidationError('Este telefone já está em uso. Por favor, insira outro válido.')