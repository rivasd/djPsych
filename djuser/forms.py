'''
Created on Mar 4, 2016

@author: Daniel Rivas / Catherine Prévost

Handles forms to edit/display subject personal info, using (I hope!) django's built-in ModelForm
see: https://docs.djangoproject.com/en/1.9/topics/forms/modelforms/#modelform
'''
from django import forms
from django.forms import ModelForm

from .models import Subject
from django.contrib.auth import get_user_model
from django.forms.fields import DateField
from allauth.account.forms import LoginForm

class SubjectForm(ModelForm):
    
    prefix= 'subject'
    birthday = DateField
    
    class Meta:
        model = Subject # the model this form should be linked to
        fields = ['student_participant_id', 'birthday', 'sex', 'occupation', 'years_of_schooling'] #a list of field names defined in the above model that should be editable via this form
        
        
        
class PublicUserForm(ModelForm):
    
    prefix = 'user'
    
    class Meta:
        model = get_user_model() # this finds the provided user model used by the built-in authentication system. It's almost always django.contrib.auth.models.User, but it's possible that someone wants to override it
        fields= ['first_name', 'last_name']
        
        
class MaterialLogin(LoginForm):
    """
    an override of the default login form that will use Material Design styling
    """
    
    pass

    
    
    
    