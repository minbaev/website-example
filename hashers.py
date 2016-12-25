'''
Created on Dec 15, 2016

@author: minbaev
'''
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class MyPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    
    iterations = PBKDF2PasswordHasher.iterations*3
    