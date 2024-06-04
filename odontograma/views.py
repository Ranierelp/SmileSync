from django.shortcuts import render
from .forms import ProcedureForm
from user.models import Dentist
from django.shortcuts import get_object_or_404

def odontograma_view(request):
    
    user = request.user
    person = request.POST.get('cpf')
    print('pesssoaaaa',person)
    if request.method == 'POST':
        procedure_form = ProcedureForm()
        
        if procedure_form.is_valid():
            procedure_form.save()
    else:
        procedure_form = ProcedureForm(user)
        
    context = {
        'procedure_form': procedure_form,
        'user': user,
    }
    
    return render(request, 'odontograma/odontograma.html', context)
