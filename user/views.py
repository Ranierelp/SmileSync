from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .forms import ClinicRegistrationForm, LoginForm
from django.http import HttpResponse

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
                    return HttpResponse('Usuário autenticado')
                
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



