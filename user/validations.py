from django.core.exceptions import ValidationError
from .models import CustomUser, Clinic, Dentist
from django import forms      
from django.db import IntegrityError

def email_unique(value):
    try:
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
    except IntegrityError:
        raise ValidationError('Erro ao salvar. Por favor, tente novamente.')

def validate_password_match(password1, password2):
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError('Senhas Diferentes')
    
def cnpj_unique(value):
    if Clinic.objects.filter(cnpj=value).exists():
        raise ValidationError('Este CNPJ já está em uso. Por favor, insira outro válido.')
    
def cro_unique(value):
    if Dentist.objects.filter(cro=value).exists():
        raise ValidationError('Este CRO já está em uso. Por favor, insira outro válido.')    
    
def user_exists(email):
    user = CustomUser.objects.filter(email=email).first()
    if user is None:
        raise forms.ValidationError('Usuário não encontrado, verifique se as credenciais estão corretas.')
    return user