from django.db import models
from address.models import Address
from odontograma.models import MedicalRecord, Procedure
from user.models import Clinic, Company


class Person(models.Model):    
    sex_user = (
    ('', 'Selecione um sexo'),
    ('1', 'Masculino'),
    ('2', 'Feminino'),
    ('3', 'Prefiro não informar'),
    ('4', 'Outro')
)
    cpf = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    rg = models.CharField(max_length=15)
    birth_date = models.DateField()
    sex = models.CharField(max_length=100, choices=sex_user, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class EletronicMedicalRecord(models.Models):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    procedute = models.ForeignKey(Procedure, on_delete=models.CASCADE)