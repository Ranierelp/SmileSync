from datetime import date, datetime
from django import forms
from address.models import Address
from user.models import Clinic, Company, CustomUser
from .models import Person
from user import validations as user_validations
from . import validations
from django.forms import Select
from odontograma.models import MedicalRecord, Procedure
from django.db import transaction

class CustomDateInput(forms.DateInput):
    """
    Classe para criar o campo de data formatado
    format_value: Função para formatar o valor do campo de data ela ultiliza a função strftime para formatar a data que é passada como valor
    para o campo de data.
    formato '%d-%m-%y' dia-mês-ano.
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['format'] = '%d-%m-%Y'
        super().__init__(*args, **kwargs)
    
    def format_value(self, value):
        if value and isinstance(value, (datetime, date)):
            return value.strftime(self.format)
        return super().format_value(value)
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

        if option.get('value') == None:
            option['attrs']['disabled'] = 'disabled'
        
        if option['value'] == '':
            option['attrs']['disabled'] = 'disabled'    
        
        return option


class PersonRegistrationForm(forms.Form):
    
    def __init__(self, clinic, *args, **kwargs):
        """
        Inicializador da classe PersonRegistrationForm.

        Args:
            clinic (Clinic): A clínica associada ao usuário logado.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.
        """
        # Chama o inicializador da classe pai (Form)
        super(PersonRegistrationForm, self).__init__(*args, **kwargs)
        # Armazena a clínica passada como argumento para uso posterior
        self.clinic = clinic
        # Filtra as empresas relacionadas à clínica logada e que estão ativas
        self.fields['empresa'].queryset = Company.objects.filter(clinic=clinic, user__is_active=True)
        self.fields['empresa'].empty_label = 'Selecione uma empresa'
        
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
    empresa = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        label='Empresa',
        widget=Select(attrs={
            'class': 'form-select', 
            'placeholder': 'Empresa'
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
    
    @transaction.atomic
    def save(self, commit=True):
        
        empresa = self.cleaned_data['empresa']
        clinica = self.clinic
        
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
            sex=self.cleaned_data['sex'],
            birth_date=self.cleaned_data['birth_date'],
            address=address,
            company=empresa,
            clinic=clinica
        )
        person.save()
        

class PersonDetailForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'birth_date', 'sex', 'company']

    def __init__(self, *args, **kwargs):
        """	
        Construtor da classe PersonDetailForm. Inicializa os campos do formulário com os dados da pessoa.
        função calculate_age para calcular a idade da pessoa e preencher o campo 'age'.
        """	
        super(PersonDetailForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome Completo',
            'readonly': 'readonly',
            'disabled': 'disabled'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'readonly': 'readonly',
            'disabled': 'disabled'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Telefone',
            'readonly': 'readonly',
            'disabled': 'disabled',
            'id': 'id_telefone'
        })
        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
            'readonly': 'readonly',
            'disabled': 'disabled'
        })
        self.fields['sex'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Sexo',
            'disabled': 'disabled'
        })
        self.fields['company'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Empresa',
            'readonly': 'readonly',
            'disabled': 'disabled'
        })
        self.fields['age'] = forms.CharField(
            label='Idade',
            initial=self.calculate_age(self.instance.birth_date),
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Idade',
                'disabled': 'disabled',
                'readonly': 'readonly'
            })
        )

    def calculate_age(self, birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


class MedicalRecordForm(forms.Form):
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
    sifilis = forms.BooleanField(
        label='Sífiles',  
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
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
    outros = forms.CharField(
        label='Outros', 
        required=False,
        max_length=100,  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Outros'
        })
    )
    frequencia_cardiaca = forms.CharField(
        label='Frequência Cardíaca',  
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Frequência Cardíaca'
        })
    )
    pressao_arterial = forms.CharField(
        label='Pressão Arterial', 
        required=False, 
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
        required=False,
        max_length=100,  
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Qual tratamento'                 
         })
    )

    def save(self, person, commit=True):
        if person.prontuario:
            medical_record = person.prontuario
        else:
            medical_record = MedicalRecord()
        
        medical_record.asma = self.cleaned_data['asma']
        medical_record.anemia = self.cleaned_data['anemia']
        medical_record.diabetes = self.cleaned_data['diabetes']
        medical_record.hipertensao = self.cleaned_data['hipertensao']
        medical_record.alergia = self.cleaned_data['alergia']
        medical_record.epilepsia = self.cleaned_data['epilepsia']
        medical_record.herpes = self.cleaned_data['herpes']
        medical_record.hiv = self.cleaned_data['hiv']
        medical_record.tuberculose = self.cleaned_data['tuberculose']
        medical_record.hepatite = self.cleaned_data['hepatite']
        medical_record.cancer = self.cleaned_data['cancer']
        medical_record.doenca_cardiaca = self.cleaned_data['doenca_cardiaca']
        medical_record.doenca_renal = self.cleaned_data['doenca_renal']
        medical_record.traumatismo_craniano = self.cleaned_data['traumatismo_craniano']
        medical_record.doencas_osseas = self.cleaned_data['doencas_osseas']
        medical_record.sifiles = self.cleaned_data['sifiles']
        medical_record.outros = self.cleaned_data['outros']
        medical_record.frequencia_cardiaca = self.cleaned_data['frequencia_cardiaca']
        medical_record.pressao_arterial = self.cleaned_data['pressao_arterial']
        medical_record.faz_tratamento_medico_atual = self.cleaned_data['faz_tratamento_medico_atual']
        medical_record.qual_tratamento = self.cleaned_data['qual_tratamento']
        
        if commit:
            medical_record.save()
            person.prontuario = medical_record
            person.save()
        return medical_record