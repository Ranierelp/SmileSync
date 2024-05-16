from django.shortcuts import render
from .forms import ProcedureForm
from user.models import Dentist
from django.shortcuts import get_object_or_404

def odontograma_view(request, dentist_pk):
    dentist = get_object_or_404(Dentist, pk=dentist_pk)
    
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProcedureForm(dentist=dentist.pk)
        
    context = {
        'form': form,
        'dentist': dentist
    }
    
    return render(request, 'odontograma/odontograma.html', context)
