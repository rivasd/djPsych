'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
from allauth.account.forms import LoginForm

def addLoginForm(request):
    return {'login_form': LoginForm()}