from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from address.models import Address

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_superuser=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_staff=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    choice_type_user = (
        ('C', 'Clínica'),
        ('E', 'Empresa'), 
        ('D', 'Dentista')
    )
    email = models.EmailField('email address', unique=True)
    phone = models.CharField('telefone', max_length=15)
    type_user = models.CharField('tipo de usuário', max_length=100, choices=choice_type_user, default='C')
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone', 'type_user']
    
    objects = UserManager()
    

class Dentist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cro = models.CharField(primary_key=True, max_length=15)

    def __str__(self):
        return f'{self.user.first_name} | {self.cro}'
    
class Clinic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cnpj = models.CharField(primary_key=True, max_length=15)
    dentista = models.ForeignKey(Dentist, on_delete=models.CASCADE)  
    
    class Meta:
        verbose_name = 'Clinic'
        verbose_name_plural = 'Clinics'
        
        
    def __str__(self):
        return self.user.first_name
    

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cnpj = models.CharField(primary_key=True, max_length=15)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return f'{self.user.first_name} | {self.cnpj}'

    