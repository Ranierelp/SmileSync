from django.shortcuts import render, redirect
from .models import Procedure, MedicalRecord, Dentist
from .forms import ProcedureForm

def odontograma_view(request):
    user = request.user

    if request.method == 'POST':
        procedure_form = ProcedureForm(user, request.POST)

        if procedure_form.is_valid():
           
            procedure = Procedure(
                procedure=procedure_form.cleaned_data['procedure'], 
                description=procedure_form.cleaned_data['description'],  
                color=procedure_form.cleaned_data['procedure'],  
                tooth_face=request.POST.get('tooth_face'), 
                number_tooth=request.POST.get('number_tooth'),  
                dentist=procedure_form.cleaned_data['dentist'], 
                medical_record=MedicalRecord.objects.get(user=user) 
            )
            procedure.save() 

            return redirect('odontograma_view')

    else:
        procedure_form = ProcedureForm(user)

    context = {
        'procedure_form': procedure_form,
        'user': user,
    }

    return render(request, 'odontograma/odontograma.html', context)

