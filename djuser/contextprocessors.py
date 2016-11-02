'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
from allauth.account.forms import LoginForm





def addLoginForm(request):
    # let us customize the login form!
    loginForm = LoginForm()
    loginForm.fields['password'].widget.attrs.update({'class':'mdl-textfield__input'})
    loginForm.fields['login'].widget.attrs.update({'class': 'mdl-textfield__input'})
    loginForm.fields['remember'].widget.attrs.update({'class':'mdl-checkbox__input'})
    
    return {'login_form': loginForm}