from typing import Any
from django import forms      
from .models import CustomUser, Clinic, Dentist, Company
from django.core.validators import MinLengthValidator
from . import validations
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import get_object_or_404

#CRIAR FUNÇÃO PARA FAZER UMA SENHA ALEATÓRIA
#CRIAR FUNÇÃO PARA ENVIAR EMAIL COM A SENHA


class ClinicRegistrationForm(forms.Form):
    name_clinic = forms.CharField(
        label='Nome da Clínica',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da Clínica',
            'id': 'id_name_clinic'
        })
    )
    cnpj = forms.CharField(
        label='CNPJ',
        validators=[validations.cnpj_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CNPJ',
            'id': 'id_cnpj'
        })
    )
    email = forms.EmailField(
        label='Email',
        validators=[validations.email_unique],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    phone = forms.CharField(
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone',
            'id': 'id_telefone'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        }),
        validators=[MinLengthValidator(6, message='Senha deve ter no mínimo 6 caracteres')]
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Senha'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        validations.validate_password_match(password1, password2)

        return cleaned_data
    
    @transaction.atomic
    def save(self, commit=True):
        
        phone_formatting = validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        cnpj_formatting = validations.remove_cnpj_formatting(self.cleaned_data['cnpj'])
        
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name = self.cleaned_data['name_clinic'],
            phone=phone_formatting,
            password=self.cleaned_data['password'],
        )
        user.save()

        clinic = Clinic.objects.create(
            user=user,
            cnpj=cnpj_formatting,
        )
        clinic.save()
        
        return user, clinic
class LoginForm(AuthenticationForm):        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        del self.fields['username']
        
    email = forms.EmailField(
        label='Email', 
        validators=[validations.user_exists],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Senha'
        })
    )
class DentistRegistrationForm(forms.Form):
    name_dentis = forms.CharField(
        label='Nome do Dentista' ,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do Denstista',
            'id': 'id_name_dentist'
        })
    )
    cro = forms.CharField(
        label='CRO',
        validators=[validations.cro_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CNPJ'
        })
    )
    email = forms.EmailField(
        label='Email',
        validators=[validations.email_unique],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    phone = forms.CharField(
        label='Telefone',
        validators=[validations.phone_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone',
            'id': 'id_telefone'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        }),
        validators=[MinLengthValidator(6, message='Senha deve ter no mínimo 6 caracteres')]
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Senha'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        validations.validate_password_match(password1, password2)

        return cleaned_data
    
    @transaction.atomic
    def save(self, clinica_logada,commit=True):
    
        phone_formatting = validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name_dentis'],
            phone=phone_formatting,
            password=self.cleaned_data['password'],
        )
        user.save()
        clinica = get_object_or_404(Clinic, cnpj=clinica_logada)
        
        dentist = Dentist.objects.create(
            user=user,
            cro=self.cleaned_data['cro'],
            clinic=clinica
        )
        dentist.save()
        
        return user, dentist
class CompanyRegistrationForm(forms.Form):
    name_company = forms.CharField(
        label='Nome da Empresa',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da Empresa',
            'id': 'id_name_company'
        })
    )
    cnpj = forms.CharField(
        label='CNPJ',
        validators=[validations.cnpj_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CNPJ',
            'id': 'id_cnpj'
        })
    )
    email = forms.EmailField(
        label='Email',
        validators=[validations.email_unique],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    phone = forms.CharField(
        label='Telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone',
            'id': 'id_telefone'
        })
    )
    street = forms.CharField(
        label='Rua',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rua'
        })
    )
    number = forms.CharField(
        label='Número',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número'
        })
    )
    neighborhood = forms.CharField(
        label='Bairro',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bairro'
        })
    )
    city = forms.CharField(
        label='Cidade',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade'
        })   
    )
    state = forms.CharField(
        label='Estado',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estado'
        })
    )
    zip_code = forms.CharField(
        label='CEP',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CEP'
        })
    )
    
    description = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição',
            'rows': 4,
        })
    )
    
    company_segment = forms.CharField(
        label='Segmento da Empresa',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Segmento da Empresa'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        }),
        validators=[MinLengthValidator(6, message='Senha deve ter no mínimo 6 caracteres')]
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Senha'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        validations.validate_password_match(password1, password2)

        return cleaned_data
    
    @transaction.atomic
    def save(self, clinica_logada,commit=True):
        
        phone_formatting = validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        cnpj_formatting = validations.remove_cnpj_formatting(self.cleaned_data['cnpj'])
        
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name = self.cleaned_data['name_company'],
            phone=phone_formatting,
            password=self.cleaned_data['password'],
        )
        user.save()
        clinica = get_object_or_404(Clinic, cnpj=clinica_logada)
        
        company = Company.objects.create(
            user=user,
            cnpj=cnpj_formatting,
            clinic=clinica
        )
        company.save()