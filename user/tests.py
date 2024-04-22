from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Clinic, Dentist, Company, Address
from django.shortcuts import get_object_or_404

CustomUser = get_user_model()

class ModelAssociationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # usuario empresa
        cls.userEmpresa = CustomUser.objects.create_user(
            email='empresa@example.com',
            name='Empresa',
            phone='123456789',
            password='password'
        )
        # usuario clinica
        cls.userClinica = CustomUser.objects.create_user(
            email='clinica@example.com',
            name='Clinica',
            phone='525252525',
            password='password'
        )
        cls.address = Address.objects.create(
            street='Rua exemplo',
            number='123',
            neighborhood='Bairro exemplo',
            city='Cidade exemplo',
            state='Estado exemplo',
            zip_code='12345678'
        )
        
        cls.clinic = Clinic.objects.create(
            user=cls.userClinica,
            cnpj='111111111',
            
        )

        clinica = get_object_or_404(Clinic, cnpj='111111111')

        cls.company = Company.objects.create(
            user=cls.userEmpresa,
            cnpj='222222222',
            company_segment='Segment',
            address=cls.address,
            clinic=clinica,
        )

    def test_dentist_clinic_association(self):
    
        dentist = Dentist.objects.create(
            user=self.userClinica,  
            cro='123456789',
            clinic=self.clinic  
        )
        self.assertEqual(dentist.clinic, self.clinic)

    def test_create_company(self):
       
        new_user_clinica = CustomUser.objects.create(
            email='clinica2@example.com',
            name='Clinica2',
            phone='888888888',
            password='password'
        )
        new_user_empresa = CustomUser.objects.create(
            email='empresa2@example.com',
            name='empresa2',
            phone='777777777',
            password='password'
        )
        new_clinica = Clinic.objects.create(
            user=new_user_clinica,
            cnpj='333333333',
        )
        new_address = Address.objects.create(
            street='Rua Patos',
            number='111',
            neighborhood='Bairro centro',
            city='Cidade Ipueira',
            state='Estado RN',
            zip_code='59315000'
        )
        new_company = Company.objects.create(
            user=new_user_empresa,
            cnpj='555555555',
            company_segment='New Segment',
            address=new_address,
            clinic=new_clinica,
        )

        self.assertIsNotNone(new_company.pk)
        self.assertEqual(new_company.user, new_user_empresa)
        self.assertEqual(new_company.cnpj, '555555555')
        self.assertEqual(new_company.company_segment, 'New Segment')
        self.assertEqual(new_company.address, new_address)
