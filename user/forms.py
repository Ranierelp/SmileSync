from django import forms      
from .models import CustomUser, Clinic, Dentist
from django.core.validators import MinLengthValidator
from . import validations

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

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.type_user = 'C'
        user.save()

        clinic = Clinic.objects.create(
            user=user,
            cnpj=self.cleaned_data['cnpj'],
        )

        return user

        
        
        