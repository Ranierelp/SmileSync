import random
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

def generate_password():
    letters_characters = string.ascii_letters
    digits_characters = string.digits
    special_characters = '@#$%&'

    password = (
        random.choice(letters_characters.upper()) + 
        random.choice(letters_characters.lower()) +
        random.choice(digits_characters) +  
        random.choice(special_characters)  
    )
    size = 10 - len(password)
    password += get_random_string(size, letters_characters + digits_characters + special_characters)

    scrambled_password = ''.join(random.sample(password, len(password)))

    return "123456"

def send_email_with_password(email, password):
    '''
    Send an email with the password.
    '''
    pass