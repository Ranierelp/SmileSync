from django.shortcuts import render
from .forms import ProcedureForm

def odontograma_view(request):
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProcedureForm()
        
    context = {'form': form}
    return render(request, 'odontograma/odontograma.html', context)
