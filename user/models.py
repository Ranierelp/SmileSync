from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from address.models import Address
from django.utils import timezone
    
class BaseModelQuerySet(models.QuerySet):

    def delete(self):
        self.update(deleted_at=timezone.now(), is_active=False)

class BaseManager(models.Manager):
    
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True, is_active=True)

class BaseModel(models.Model):
    class Meta:
        abstract = True
        
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de Modificação ', auto_now=True)
    deleted_at = models.DateTimeField('Data de Deleção', editable=False, blank=True, null=True)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Membro da equipe', default=False)

    objects = BaseManager()
    
    def delete(self, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
        
    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)
class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
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
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_staff=True e is_superuser=True')
        
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail',unique=True )
    phone = models.CharField('Telefone', max_length=15)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    
    objects = UserManager()
    
    def soft_delete(self):
        self.delete()

class Clinic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cnpj = models.CharField(primary_key=True, max_length=15) 
    
    class Meta:
        verbose_name = 'Clinic'
        verbose_name_plural = 'Clinics'
            
    def __str__(self):
        return self.user.name
class Dentist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cro = models.CharField(primary_key=True, max_length=15)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name}'
    
    
class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cnpj = models.CharField(primary_key=True, max_length=15)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    description = models.TextField('Descrição', max_length=500, blank=True, null=True)
    company_segment = models.CharField('Segmento da Empresa', max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return f'{self.user.name}'

    