from django import forms      
from .models import CustomUser, Clinic, Dentist, Company, Address
from django.core.validators import MinLengthValidator
from . import validations
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import get_object_or_404
from .utils import generate_password
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role

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
        assign_role(user, 'clinica')
          
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
    
    @transaction.atomic
    def save(self, clinica_logada,commit=True):
    
        phone_formatting = validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        password = generate_password()
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name_dentis'],
            phone=phone_formatting,
            password=password,
        )
        user.save()
        clinica = get_object_or_404(Clinic, cnpj=clinica_logada)
        
        dentist = Dentist.objects.create(
            user=user,
            cro=self.cleaned_data['cro'],
            clinic=clinica
        )
        dentist.save()    
        assign_role(user, 'dentista')
         
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
        validators=[validations.phone_unique],
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
            'placeholder': 'CEP',
            'pattern':'\d{5}-\d{3}'
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
    
    @transaction.atomic
    def save(self, clinica_logada,commit=True):
        
        phone_formatting = validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        cnpj_formatting = validations.remove_cnpj_formatting(self.cleaned_data['cnpj'])
        zip_code_formatting = validations.remove_zip_code_formatting(self.cleaned_data['zip_code'])
        password = generate_password()
        print(f'Senha gerada: {password}')
        
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            name = self.cleaned_data['name_company'],
            phone=phone_formatting,
            password=password,
        )
        user.save()
        clinica = get_object_or_404(Clinic, cnpj=clinica_logada)
        
        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            neighborhood=self.cleaned_data['neighborhood'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=zip_code_formatting
        )
        address.save()
        company = Company.objects.create(
            user=user,
            cnpj=cnpj_formatting,
            clinic=clinica,
            address=address,
            description=self.cleaned_data['description'],
            company_segment=self.cleaned_data['company_segment']
        )
        company.save()
        assign_role(user, 'empresa')
    
class ProfileForm(forms.Form):
    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome',
            'id': 'id_name'
        })
    )
    email = forms.EmailField(
        label='Email',
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
    # identifier = forms.CharField(
    #     label='CRO/CNPJ',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'CRO/CNPJ',
    #         'id': 'id_identifier',
    #         'disabled': 'disabled'
    #     })
    # )
    
    cnpj = forms.CharField(
        label='CNPJ',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CNPJ',
            'id': 'id_cnpj',
            'readonly': 'readonly'
        })
    )
    
    cro = forms.CharField(
        label='CRO',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CRO',
            'id': 'id_cro',
            'readonly': 'readonly'
        })
    )
    
    photo = forms.FileField(
        label='Foto',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id':'picture_input'
        })
    )

    def save(self, user):
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.photo = self.cleaned_data['photo']
        if has_role(user, 'empresa'):
            user.company.cnpj = self.cleaned_data['cnjp']
        if has_role(user, 'dentista'):
            user.dentist.cro = self.cleaned_data['cro']
        if has_role(user, 'clinica'):
            user.clinic.cnpj = self.cleaned_data['cnpj']
        user.save()