from django import forms  

class ProcedureForm(forms.Form):
    procedure = forms.CharField(
        label='Procedimento', 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Procedimento',
        })
    )
    
    description = forms.CharField(
        label='Descrição',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição',
        })
    )
    
    dentist = forms.CharField(
        label='Dentista',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dentista',
        })
    )
    
    
    
    
    
    