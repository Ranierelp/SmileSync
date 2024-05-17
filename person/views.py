from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from person.models import Person
from .forms import PersonDetailForm, PersonRegistrationForm, MedicalRecordForm
from odontograma.forms import ProcedureForm

@login_required
def create_person_view(request):
    """ Função para criar a view de criação de pessoa

    Args:
        request ([HttpRequest]): [Requisição HTTP]

    Returns:
        [HttpResponse]: [Resposta HTTP]
    """

    # Verificando se a requisição é do tipo POST
    if request.method == 'POST':
        # Criando o formulário de pessoa
        form = PersonRegistrationForm(request.user.clinic, request.POST)

        # Verificando se o formulário é válido
        if form.is_valid():
            form.save()
            alert_sucess = 'Paciente cadastrado com sucesso!'
            form = PersonRegistrationForm(request.user.clinic)
            context = {
                'form': form,
                'success': True,
                'alert_sucess': alert_sucess
            }

            return render(request, 'person/register_person.html', context)
    else:
        # Criando o formulário de pessoa
        form = PersonRegistrationForm(request.user.clinic)

    # Renderizando o template de criação de pessoa
    return render(request, 'person/register_person.html', {'form': form})


@login_required
def person_create_medical_record_view(request, cpf):
    person = get_object_or_404(Person, cpf=cpf)
    custom_user = request.user
    
    if request.method == 'POST':
        medical_record_form = MedicalRecordForm(request.POST)
        procedure_form = ProcedureForm(request.POST, custom_user)
       
        
        if medical_record_form.is_valid():
            medical_record = medical_record_form.save(person ,commit=False)
            if not person.prontuario:
                medical_record.save()
                person.prontuario = medical_record
            else:
                medical_record.pk = person.prontuario.pk
                medical_record.save()
                
            person.save()
            alert_sucess = 'Prontuário do paciente finalizada com sucesso!'
            
            context = {
                'form': PersonDetailForm(instance=person), 
                'procedure_form': procedure_form,
                'medical_record_form': medical_record_form,
                'person': person,
                'user': custom_user,
                'alert_sucess': alert_sucess,
                'success': True
            }
            return render(request, 'person/medical_record.html', context)
    
    else:
        form = PersonDetailForm(instance=person)
        procedure_form = ProcedureForm(request.POST, custom_user)
        
        # Se a pessoa já tiver um prontuário, preenche o formulário com os dados existentes
        initial_data = {
            'anemia': person.prontuario.anemia,
            'hipertensao': person.prontuario.hipertensao,
            'alergia': person.prontuario.alergia,
            'epilepsia': person.prontuario.epilepsia,
            'herpes': person.prontuario.herpes,
            'hiv': person.prontuario.hiv,
            'tuberculose': person.prontuario.tuberculose,
            'hepatite': person.prontuario.hepatite,
            'cancer': person.prontuario.cancer,
            'doenca_cardiaca': person.prontuario.doenca_cardiaca,
            'doenca_renal': person.prontuario.doenca_renal,
            'traumatismo_craniano': person.prontuario.traumatismo_craniano,
            'doencas_osseas': person.prontuario.doencas_osseas,
            'sifiles': person.prontuario.sifilis,
            'asma': person.prontuario.asma,
            'diabetes': person.prontuario.diabetes,
            'outros': person.prontuario.outros,
            'frequencia_cardiaca': person.prontuario.frequencia_cardiaca,
            'pressao_arterial': person.prontuario.pressao_arterial,
            'faz_tratamento_medico_atual': person.prontuario.faz_tratamento_medico_atual,
            'qual_tratamento': person.prontuario.qual_tratamento,
        } if person.prontuario else {}
        medical_record_form = MedicalRecordForm(initial=initial_data)
    
    context = {
        'form': form,  
        'procedure_form': procedure_form,
        'medical_record_form': medical_record_form,
        'person': person,
        'user': custom_user
    }
    return render(request, 'person/medical_record.html', context)

@login_required
def person_detail_view(request):
    form = None
    person = None
    medical_record_form = None
    cpf = request.GET.get('cpf')
    custom_user = request.user
    procedure_form = ProcedureForm(custom_user)

    
    if cpf:
        person = get_object_or_404(Person, cpf=cpf)
        form = PersonDetailForm(instance=person)
        procedure_form = ProcedureForm(custom_user)
        
        initial_data = {
            'anemia': person.prontuario.anemia,
            'hipertensao': person.prontuario.hipertensao,
            'alergia': person.prontuario.alergia,
            'epilepsia': person.prontuario.epilepsia,
            'herpes': person.prontuario.herpes,
            'hiv': person.prontuario.hiv,
            'tuberculose': person.prontuario.tuberculose,
            'hepatite': person.prontuario.hepatite,
            'cancer': person.prontuario.cancer,
            'doenca_cardiaca': person.prontuario.doenca_cardiaca,
            'doenca_renal': person.prontuario.doenca_renal,
            'traumatismo_craniano': person.prontuario.traumatismo_craniano,
            'doencas_osseas': person.prontuario.doencas_osseas,
            'sifiles': person.prontuario.sifilis,
            'asma': person.prontuario.asma,
            'diabetes': person.prontuario.diabetes,
            'outros': person.prontuario.outros,
            'frequencia_cardiaca': person.prontuario.frequencia_cardiaca,
            'pressao_arterial': person.prontuario.pressao_arterial,
            'faz_tratamento_medico_atual': person.prontuario.faz_tratamento_medico_atual,
            'qual_tratamento': person.prontuario.qual_tratamento,
        } if person.prontuario else {}
        medical_record_form = MedicalRecordForm(initial=initial_data)
        
            
    context = {
        'procedure_form': procedure_form,
        'form': form,
        'medical_record_form': medical_record_form,
        'person': person,
        'user': custom_user
    }
    
    return render(request, 'person/medical_record.html', context)
