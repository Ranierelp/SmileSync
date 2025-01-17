from django import forms  
from django.forms import Select
from user.models import Dentist
from rolepermissions.checkers import has_role

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

class ProcedureForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        """
        Inicializador da classe PersonRegistrationForm.

        Args:
            clinic (Clinic): A clínica associada ao usuário logado.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.
        """

        # Chama o inicializador da classe pai (Form)
        super(ProcedureForm, self).__init__(*args, **kwargs)
        
        self.user = user
                
        if has_role(user, 'clinica'):
            # Filtra as dentista relacionadas à clínica logada e que estão ativas
            self.fields['dentist'].queryset = Dentist.objects.filter(clinic=user.clinic.pk, user__is_active=True)
            self.fields['dentist'].empty_label = 'Selecione o Dentista'
        else:

            # Filtra as dentista relacionadas à clínica logada e que estão ativas
            self.fields['dentist'].queryset = Dentist.objects.filter(user=user, user__is_active=True)
            self.fields['dentist'].empty_label = 'Selecione o Dentista'
            
    
    procedure = forms.ChoiceField(
        label='Procedimento',
        choices=[
            ('', 'Selecione um procedimento'),
            ('#0000FF', 'Limpeza - Azul'),             
            ('#FF0000', 'Extração de Dente - Vermelho'), 
            ('#FFFFFF', 'Obturação - Branco'),        
            ('#FFFF00', 'Canal - Amarelo'),            
            ('#008000', 'Coroa Dentária - Verde'),     
            ('#FFA500', 'Implante Dentário - Laranja'),
            ('#800080', 'Ortodontia - Roxo'),          
            ('#FFFFFF', 'Clareamento Dental - Branco'),
            ('#808080', 'Procedimento Cirúrgico - Cinza'), 
            ('#FFC0CB', 'Tratamento de Gengiva - Rosa')    
        ],
        widget=Select(attrs={
            'class': 'form-control',
        })
    )
    
    description = forms.CharField(
        label='Descrição',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição',
        })
    )
    
    dentist = forms.ModelChoiceField(
        queryset=Dentist.objects.none(),
        label='Dentista',
        widget=Select(attrs={
            'class': 'form-control',
            'placeholder': 'Dentista',
        })
    )
    

    
    
    
    
    