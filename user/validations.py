from django.core.exceptions import ValidationError
from .models import CustomUser, Clinic, Dentist, Company
from django import forms      
from django.db import IntegrityError
from django.db.models import Model

def email_unique(value:str) :
    try:
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
    except IntegrityError:
        raise ValidationError('Erro ao salvar. Por favor, tente novamente.')

def validate_password_match(password1, password2:str):
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError('Senhas Diferentes')
    
def phone_unique(value:str):
    if CustomUser.objects.filter(phone=value).exists():
        raise forms.ValidationError('Este telefone já está em uso. Por favor, insira outro válido.')   

def cnpj_unique(model:Model, value:str):
    if model.objects.filter(cnpj=value).exists():
        raise forms.ValidationError('Este CNPJ já está em uso. Por favor, insira outro válido.')
    
def cro_unique(value:str):
    if Dentist.objects.filter(cro=value).exists():
        raise ValidationError('Este CRO já está em uso. Por favor, insira outro válido.')    
    
def user_exists(email:str):
    user = CustomUser.objects.filter(email=email).first()
    if user is None:
        raise forms.ValidationError('Usuário não encontrado, verifique se as credenciais estão corretas.')
    return user

def remove_cnpj_formatting(cnpj:str):
    cnpj_unformatted = cnpj.replace(".", "").replace("/", "").replace("-", "")
    return cnpj_unformatted

def remove_phone_number_formatting(phone_number:str):
    phone_number_unformatted = phone_number.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
    return phone_number_unformatted

def remove_zip_code_formatting(zip_code:str):
    zip_code_unformatted = zip_code.replace("-", "")
    return zip_code_unformatted


# VERIFICAR AS VALIDAÇÕES DOS FORMS !!!!!!!!!!