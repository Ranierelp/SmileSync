from django.db import models
from user.models import Dentist

class MedicalRecord(models.Model):
    asma = models.BooleanField()
    anemia = models.BooleanField()
    diabetes = models.BooleanField()
    hipertensao = models.BooleanField()
    alergia = models.BooleanField()
    epilepsia = models.BooleanField()
    herpes = models.BooleanField()
    hiv = models.BooleanField()
    tuberculose = models.BooleanField()
    hepatite = models.BooleanField()
    cancer = models.BooleanField()
    doenca_cardiaca = models.BooleanField()
    doenca_renal = models.BooleanField()
    traumatismo_craniano = models.BooleanField()
    doencas_osseas = models.BooleanField()
    sifiles = models.BooleanField()
    outros = models.CharField(max_length=100)
    frequencia_cardiaca = models.CharField(max_length=100)
    pressao_arterial = models.CharField(max_length=100)
    faz_tratamento_medico_atual = models.BooleanField()
    qual_tratamento = models.CharField(max_length=100)

class Procedure(models.Model):
    procedure = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=100)
    tooth_face = models.CharField(max_length=100)
    number_tooth = models.IntegerField()
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='procedures')
    
    def __str__(self):
        return self.procedure 
       
