from django import forms

from address.models import Address
from user.models import Clinic, Company
from .models import Person
from user import validations as user_validations
from . import validations
from django.forms import Select
from odontograma.models import MedicalRecord, Procedure

class Select(Select):
    """ Classe para criar o campo de select formatado

    Args:
        Select ([Select]): [Campo de select Django]
    """

    def create_option(self, *args, **kwargs):
        """ Função para criar o campo de select formatado

        Returns:
            [dict]: [Campo de select formatado]
        """

        # Criando o campo de select formatado
        option = super().create_option(*args, **kwargs)

        # Desabilitando a opção de seleção
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        if option.get('value') == 2:
            option['attrs']['disabled'] = 'disabled'

        return option


class PersonRegistrationForm(forms.Form):
    name = forms.CharField(
        label='Nome Completo', 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome Completo',
        })
    )
    email = forms.EmailField(
        label='Email',
        validators=[validations.person_email_unique],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    cpf = forms.CharField(
        label='CPF',
        validators=[validations.cpf_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CPF',
            'pattern':'\d{3}\.\d{3}\.\d{3}-\d{2}'
        })
    )
    phone = forms.CharField(
        label='Telefone',
        validators=[validations.person_phone_unique],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone',
            'id': 'id_telefone'
        })
    )
    rg = forms.CharField(
        label='RG',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'RG'
        })
    )
    birth_date = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Data de Nascimento',
            'type': 'date'
        })
    )
    sex = forms.ChoiceField(
        label='Sexo',
        choices=(
            ('', 'Selecione um sexo'),
            ('1', 'Masculino'),
            ('2', 'Feminino'),
            ('3', 'Prefiro não informar'),
            ('4', 'Outro')
        ),
        widget=Select(
        attrs={
            'class':'form-select', 'placeholder':'Sexo'
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
    asma = forms.BooleanField(
        label='Asma',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    diabetes = forms.BooleanField(
        label='Diabetes',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def save(self, clinica, commit=True):
        
        company =  Company.objects.get(cnpj='00000000011111')
        clinica = Clinic.objects.get(cnpj=clinica)
        
        phone_formatting = user_validations.remove_phone_number_formatting(self.cleaned_data['phone'])
        zip_code_formatting = user_validations.remove_zip_code_formatting(self.cleaned_data['zip_code'])
        cpf_formatting = validations.remove_cpf_formatting(self.cleaned_data['cpf'])
        
        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            neighborhood=self.cleaned_data['neighborhood'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=zip_code_formatting
        )
        address.save()
        person = Person(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            cpf=cpf_formatting,
            phone=phone_formatting,
            rg=self.cleaned_data['rg'],
            birth_date=self.cleaned_data['birth_date'],
            address=address,
            company=company,
            clinic=clinica
        )
        person.save()
        
class FormMedicalRecord(forms.Form):
    anemia = forms.BooleanField(
        label='Anemia',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    hipertensao = forms.BooleanField(
        label='Hipertensão',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    alergia = forms.BooleanField(
        label='Alergia',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    epilepsia = forms.BooleanField(
        label='Epilepsia',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    herpes = forms.BooleanField(
        label='Herpes',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    hiv = forms.BooleanField(
        label='HIV',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    tuberculose = forms.BooleanField(
        label='Tuberculose',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    hepatite = forms.BooleanField(
        label='Hepatite',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    cancer = forms.BooleanField(
        label='Câncer',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    doenca_cardiaca = forms.BooleanField(
        label='Doença Cardíaca',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    doenca_renal = forms.BooleanField(
        label='Doença Renal',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    traumatismo_craniano = forms.BooleanField(
        label='Traumatismo Craniano',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    doencas_osseas = forms.BooleanField(
        label='Doenças Ósseas',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    sifiles = forms.BooleanField(
        label='Sífiles',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    outros = forms.CharField(
        label='Outros',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Outros'
        })
    )
    frequencia_cardiaca = forms.CharField(
        label='Frequência Cardíaca',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Frequência Cardíaca'
        })
    )
    pressao_arterial = forms.CharField(
        label='Pressão Arterial',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pressão Arterial'
        })
    )
    faz_tratamento_medico_atual = forms.BooleanField(
        label='Faz tratamento médico atual',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    qual_tratamento = forms.CharField(
        label='Qual tratamento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qual tratamento'
        })
    )
    
