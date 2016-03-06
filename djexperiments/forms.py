'''
Created on Mar 4, 2016

@author: Daniel Rivas
'''

from django import forms
from django.utils.translation import ugettext_lazy as l_

class SandboxForm(forms.Form):
    
    prefix='sandbox'
    def __init__(self, versions, *args, **kwargs):
        super(SandboxForm, self).__init__(*args, **kwargs)
        self.fields['version'].choices=versions
        
    version = forms.ChoiceField(label=l_("Which configuration would you like to try?"))
    
    format_choices =(
        ('json', 'JSON'),
        ('csv', 'CSV')
    )
    format = forms.ChoiceField(label=l_("Display data in format"), choices=format_choices)
    