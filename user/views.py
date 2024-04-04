from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .forms import ClinicRegistrationForm, LoginForm, DentistRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def clinic_register_view(request):
    if request.method == 'POST':
        form = ClinicRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/register.html', {'form': ClinicRegistrationForm(), 'success': True})
    else:
        form = ClinicRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/user/home')
                
                else:
                    form.add_error(None, 'Email ou senha inválidos')
                    
            except ValidationError as e:
                form.add_error(None, str(e))
                
    else:
        form = LoginForm()
    
    context = {'form': form}
    
    return render(request, 'users/login.html', context)

def home_view(request):
    return render(request, 'users/home.html')

def create_dentist_view(request):
    if request.method == 'POST':
        form = DentistRegistrationForm(request.post)
        if form.is_valid():
            form.save()
            return HttpResponse('Dentista criado com sucesso')
    else:
        form = DentistRegistrationForm()
    
    context = {'form': form}
    return render(request, 'users/register_dentist.html', context)
    

def list_dentist_view(request):
    return HttpResponse('Lista de dentistas')

def update_dentist_view(request):
    return HttpResponse('Dentista atualizado com sucesso')

def delete_dentist_view(request):
    return HttpResponse('Dentista deletado com sucesso')