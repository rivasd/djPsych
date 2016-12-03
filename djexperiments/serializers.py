'''
Created on Dec 1, 2016

@author: Daniel Rivas
'''

from rest_framework import serializers
from .models import Experiment

class ExperimentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Experiment
        fields=('label', 'id', 'verbose_name', 'description', 'estimated_length', 'allow_repeats', 'max_repeats', 'enforce_finish', 'compensated', 
                'max_payouts', 'allow_do_overs', 'funds_remaining', 'is_active')
