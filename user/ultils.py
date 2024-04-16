import random
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def generate_password():
    '''
    Generate a random password with 8 characters.
    '''
    return get_random_string(length=8, allowed_chars=string.ascii_letters + string.digits)

def send_email_with_password(email, password):
    
    
    
    
    '''
    Send an email with the password.
    '''
    pass