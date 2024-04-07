import secrets
import string
import random
import subprocess

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation

selection_list = letters + digits + special_chars
password_len = int(subprocess.check_output(['shuf', '-i', '16-32', '-n', '1']))

while True:
    password = ''
    for i in range(password_len):
        password += ''.join(secrets.choice(selection_list))

    if (any(char in special_chars for char in password) and sum(char in digits for char in password)>=2):
        break
    
print(password)
