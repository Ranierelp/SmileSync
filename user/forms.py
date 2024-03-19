from django import forms      
from django.forms import Select
from .models import CustomUser, Clinic, Dentist
from django.contrib.auth import get_user_model

from django import forms
from .models import CustomUser, Clinic

class ClinicRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password']

    name_clinic = forms.CharField(label='Nome da Clínica', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nome da Clínica'}))
    cnpj = forms.CharField(label='CNPJ', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CNPJ'}))
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Senhas não conferem')

        return cleaned_data

    def save(self, commit=True):
        user = CustomUser.objects.create(
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            password=self.cleaned_data['password'],
            type_user='C'  # Set type_user here
        )
        clinic = Clinic.objects.create(
            user=user,
            name=self.cleaned_data['name_clinic'],
            cnpj=self.cleaned_data['cnpj'],
        )
        return clinic


        
        
        