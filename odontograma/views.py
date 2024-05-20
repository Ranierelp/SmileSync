from django.shortcuts import render
from .forms import ProcedureForm
from user.models import Dentist
from django.shortcuts import get_object_or_404

def odontograma_view(request):
    print('odontograma_view')
    user = request.user
    
    if request.method == 'POST':
        procedure_form = ProcedureForm(request.POST, user)
        print('asdasdasdas')
        if procedure_form.is_valid():
            procedure_form.save()
    else:
        procedure_form = ProcedureForm(user)
        
    context = {
        'procedure_form': procedure_form,
        'user': user,
    }
    
    return render(request, 'odontograma/odontograma.html', context)
