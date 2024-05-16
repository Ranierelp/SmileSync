import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .forms import ClinicRegistrationForm, LoginForm, DentistRegistrationForm, CompanyRegistrationForm, ProfileForm
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser, Dentist, Company
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from rolepermissions.checkers import has_role
from . import validations  

def clinic_register_view(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ClinicRegistrationForm(request.POST)
        if form.is_valid():
            cnpj_formatado = validations.remove_cnpj_formatting(form.cleaned_data['cnpj'])
            if validations.cnpj_unique(cnpj_formatado):
                    form.add_error('cnpj', 'Este CNPJ já está em uso. Por favor, insira outro válido.')
            else:
                form.save()
                alert_sucess = 'Clinica cadastrada com sucesso!'
                context = {
                    'form': form,
                    'success': True,
                    'alert_sucess': alert_sucess
                }
                return render(request, 'users/register.html', context)
    else:
        form = ClinicRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

def login_view(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/user/home/')
                else:
                    form.add_error(None, 'Email ou senha inválidos')
                    
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = LoginForm()
    
    context = {'form': form}
    
    return render(request, 'users/login.html', context)

@login_required
def home_view(request:HttpRequest) -> HttpResponse:
    return render(request, 'users/home.html')

@login_required
def create_dentist_view(request:HttpRequest) -> HttpResponse:
    if has_role(request.user, 'clinica'):   
        if request.method == 'POST':
            form = DentistRegistrationForm(request.POST)
            if form.is_valid():
                clinica = request.user.clinic.cnpj
                form.save(clinica)
                alert_sucess = 'Dentista cadastrado com sucesso!'
                context = {
                    'form': form,
                    'success': True,
                    'alert_sucess': alert_sucess
                }
                return render(request,'users/register_dentist.html', context)
        else:
            form = DentistRegistrationForm()
            
        context = {'form': form}
        return render(request, 'users/register_dentist.html', context)
    
    else:
        logout(request)
        return render(request, '403.html')

@login_required
def logout_view(request:HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/user/login/')  

@login_required
def list_dentists_view(request:HttpRequest) -> HttpResponse:
    if has_role(request.user, 'clinica'):
        dentista = Dentist.objects.filter(clinic=request.user.clinic, user__is_active=True )
        context = {
            'dentista': dentista
        }	
        return render(request, 'users/list_dentist.html', context)
    else:
        logout(request)
        return render(request, '403.html')

@login_required
def update_dentist_view(request:HttpRequest) -> HttpResponse:
    return HttpResponse('Dentista atualizado com sucesso')

@login_required
def delete_dentist_view(request, pk) -> HttpResponse:
    if has_role(request.user, 'clinica'):    
        dentist = get_object_or_404(Dentist, pk=pk)
        
        if request.method == 'POST':
            try:
                dentist.user.soft_delete()
                response_data = {'status': 'success', 'message': 'Dentista deletado com sucesso.'}
            except Exception as e:
                response_data = {'status': 'error', 'message': str(e)}
            return JsonResponse(response_data, status=200)

        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
    else:
        logout(request)
        return render(request, '403.html', status=403)

@login_required
def create_company_view(request:HttpRequest) -> HttpResponse:
    if has_role(request.user, 'clinica'): 
        if request.method == 'POST':
            form = CompanyRegistrationForm(request.POST)
            if form.is_valid():
                cnpj_formatado = validations.remove_cnpj_formatting(form.cleaned_data['cnpj'])
                if validations.cnpj_unique(cnpj_formatado):
                    form.add_error('cnpj', 'Este CNPJ já está em uso. Por favor, insira outro válido.')
                else:
                    clinica = request.user.clinic.cnpj
                    form.save(clinica)
                    alert_sucess = 'Empresa cadastrada com sucesso!'
                    context = {
                        'form': form,
                        'success': True,
                        'alert_sucess': alert_sucess
                    }
                    return render(request, 'users/register_company.html', context)
        else:
            form = CompanyRegistrationForm()
        
        context = {'form': form}
        return render(request, 'users/register_company.html', context)
    
    else:
        logout(request)
        return render(request, '403.html', status=403)

@login_required
def list_companies_view(request:HttpRequest) -> HttpResponse:
    if has_role(request.user, 'clinica'):
        empresas = Company.objects.filter(clinic=request.user.clinic, user__is_active=True)
        context = {
            'empresas': empresas
        }
        return render(request, 'users/list_companies.html', context)
    else:
        logout(request)
        return render(request, '403.html')

@login_required
def delete_company_view(request, pk) -> HttpResponse:
    if has_role(request.user, 'clinica'): 
        company = get_object_or_404(Company, pk=pk)
        
        if request.method == 'POST':
            try:
                company.user.soft_delete()
                response_data = {'status': 'success', 'message': 'Empresa deletada com sucesso.'}
            except Exception as e:
                response_data = {'status': 'error', 'message': str(e)}
            return JsonResponse(response_data, status=200)

        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
    else:
        logout(request)
        return render(request, '403.html', status=403)

def planos_view(request):
    return render(request,'users/plano.html')
    
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user)
            context = {
                'form': form,
                'success': True,
                'alert_sucess': 'Perfil atualizado com sucesso!'
            }
            return render(request, 'users/profile.html', context)
    else:
        initial_data = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'photo': user.photo if user.photo else ''
        }
        if has_role(user, 'dentista'):
            initial_data['cro'] = user.dentist.cro
        elif has_role(user, 'empresa'):
            initial_data['cnpj'] = user.company.cnpj
        elif has_role(user, 'clinica'):
            initial_data['cnpj'] = user.clinic.cnpj
        
        form = ProfileForm(initial=initial_data)
        
    context = {
        'form': form
    }
        
    return render(request, 'users/profile.html', context)   