from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .forms import ClinicRegistrationForm, LoginForm, DentistRegistrationForm, CompanyRegistrationForm
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser, Dentist, Company

def clinic_register_view(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ClinicRegistrationForm(request.POST)
        if form.is_valid():
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

@login_required
def logout_view(request:HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/user/login/')  

@login_required
def list_dentists_view(request:HttpRequest) -> HttpResponse:
    dentista = Dentist.objects.filter(clinic=request.user.clinic)
    context = {
        'dentista': dentista
    }	
    return render(request, 'users/list_dentist.html', context)

@login_required
def update_dentist_view(request:HttpRequest) -> HttpResponse:
    return HttpResponse('Dentista atualizado com sucesso')

@login_required
def delete_dentist_view(request:HttpRequest) -> HttpResponse:
    return HttpResponse('Dentista deletado com sucesso')

@login_required
def create_company_view(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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

@login_required
def list_companies_view(request:HttpRequest) -> HttpResponse:
    empresas = Company.objects.filter(clinic=request.user.clinic)
    context = {
        'empresas': empresas
    }
    return render(request, 'users/list_companies.html', context)