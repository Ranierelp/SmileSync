from typing import Any
from django import forms      
from .models import CustomUser, Clinic, Dentist
from django.core.validators import MinLengthValidator
from . import validations
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import get_object_or_404

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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone'
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
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name = self.cleaned_data['name_clinic'],
            phone=self.cleaned_data['phone'],
            password=self.cleaned_data['password'],
        )
        user.save()

        clinic = Clinic.objects.create(
            user=user,
            cnpj=self.cleaned_data['cnpj'],
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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone'
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
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name = self.cleaned_data['name_dentis'],
            phone=self.cleaned_data['phone'],
            password=self.cleaned_data['password'],
        )
        user.save()
        clinica = get_object_or_404(Clinic, cnpj=clinica_logada)
        print(clinica)
        
        dentist = Dentist.objects.create(
            user=user,
            cro=self.cleaned_data['cro'],
            clinic=clinica
        )
        dentist.save()
        
        return user, dentist
        