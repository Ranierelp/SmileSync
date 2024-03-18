from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10, blank=True, default="S/N")
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        
    def __str__(self):
        return f' {self.street}, {self.number}, {self.neighborhood}, {self.city}, {self.state} - {self.zip_code}'
    