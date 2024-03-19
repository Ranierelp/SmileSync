from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClinicRegistrationForm

def clinic_register(request):
    if request.method == 'POST':
        form = ClinicRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/register.html', {'form': ClinicRegistrationForm(), 'success': True})
    else:
        form = ClinicRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def clinic_login(request):
    return render(request, 'users/login.html')
