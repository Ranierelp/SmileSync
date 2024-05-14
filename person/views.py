from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect

from person.models import Person
from .forms import PersonDetailForm, PersonRegistrationForm, MedicalRecordForm

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


def create_medical_record(request):
    """ Função para criar o prontuário médico

    Args:
        request ([HttpRequest]): [Requisição HTTP]

    Returns:
        [HttpResponse]: [Resposta HTTP]
    """

    # Verificando se a requisição é do tipo POST
    if request.method == 'POST':
        # Criando o formulário de prontuário médico
        form = MedicalRecordForm(request.POST)

        # Verificando se o formulário é válido
        if form.is_valid():
            form.save()
            alert_sucess = 'Prontuário médico cadastrado com sucesso!'
            context = {
                'form': form,
                'success': True,
                'alert_sucess': alert_sucess
            }

            return render(request, 'person/register_medical_record.html', context)
    else:
        # Criando o formulário de prontuário médico
        form = MedicalRecordForm()

    # Renderizando o template de criação de prontuário médico
    return render(request, 'person/register_medical_record.html', {'form': form})

def person_detail_and_update_view(request):
    """ Função para detalhar e atualizar uma pessoa

    Args:
        request ([HttpRequest]): [Requisição HTTP]
        person_id ([int]): [ID da pessoa]

    Returns:
        [HttpResponse]: [Resposta HTTP]
    """
  
    # Buscando a pessoa pelo ID
    cpf = request.GET.get('cpf')
    if cpf:
        person = Person.objects.get(pk=cpf)

    # Verificando se a requisição é do tipo POST
    if request.method == 'POST':
        # Criando o formulário de pessoa
        form = PersonDetailForm(request.user.clinic, request.POST, instance=person)

        # Verificando se o formulário é válido
        if form.is_valid():
            form.save()
            alert_sucess = 'Paciente atualizado com sucesso!'
            context = {
                'form': form,
                'success': True,
                'alert_sucess': alert_sucess
            }

            return render(request, 'person/register_person.html', context)
    else:
        # Criando o formulário de pessoa
        form = PersonDetailForm(request.user.clinic, instance=person)

    # Renderizando o template de detalhe e atualização de pessoa
    return render(request, 'person/medical_record.html', {'form': form})


def person_detail_view(request):
    form = None
    medical_record_form = None
    person = None
    cpf = request.GET.get('cpf')

    if cpf:
        person = get_object_or_404(Person, cpf=cpf)
        form = PersonDetailForm(instance=person)
        medical_record_form = MedicalRecordForm()
        
    if request.method == 'POST' and person:
        form = PersonDetailForm(request.POST, instance=person)
        medical_record_form = MedicalRecordForm(request.POST)

        if form.is_valid() and medical_record_form.is_valid():
            form.save()
            context = {
                'form': form,
                'medical_record_form': medical_record_form,
                'person': person,
                'success': True,
                'alert_sucess': 'Ficha do paciente finalizada com sucesso!'
            }
            return render(request, 'person/medical_record.html', context)
            
    context = {
        'form': form,
        'medical_record_form': medical_record_form,
        'person': person
    }
    
    return render(request, 'person/medical_record.html',context)