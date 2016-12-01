'''
Created on Dec 1, 2016

@author: Daniel Rivas
'''

from rest_framework import serializers
from .models import Experiment

class ExperimentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Experiment
        fields="__all__"
