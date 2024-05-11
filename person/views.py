from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import PersonRegistrationForm

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
        form = PersonRegistrationForm(request.POST)

        # Verificando se o formulário é válido
        if form.is_valid():
            clinica = request.user.clinic.cnpj
            form.save(clinica)
            alert_sucess = 'Paciente cadastrado com sucesso!'
            context = {
                'form': form,
                'success': True,
                'alert_sucess': alert_sucess
            }
            # Redirecionando para a página de listagem de pessoas
            return render(request, 'person/register_person.html', context)
    else:
        # Criando o formulário de pessoa
        form = PersonRegistrationForm()

    # Renderizando o template de criação de pessoa
    return render(request, 'person/register_person.html', {'form': form})
