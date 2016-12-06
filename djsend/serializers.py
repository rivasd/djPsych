'''
Created on 6 déc. 2016

@author: Daniel Rivas
'''

from rest_framework import serializers
from django.db.models.query import QuerySet


class BlockSerializer(serializers.ModelSerializer):
    """
    Another generic modelSerializers, meant for block models
    """ 
    
    class Meta:
        model = None
        fields = '__all__'
    
    def __init__(self, instance=None, *args, **kwargs):
        
        super(BlockSerializer, self).__init__(*args, **kwargs)
        kind = type(instance)
        if kind == QuerySet or kind == list: # the first argument may be a list/queryset instead of a single object to serialize
            kind = type(instance[0])
        self.Meta.model = kind
        

class ConfigSerializer(serializers.ModelSerializer):
    """
    Generic serializer for experimental configuration.
    A ModelSerializer but whose model is not set in advance, you need to assign it at object instatiation time
    
    """
    
    blocks = serializers.SerializerMethodField('get_blocks')
    
    
    class Meta:
        model = None # the model is left unspecified, you must specify it when instatiating the serializer, see: https://blog.hipwerk.com/django-rest-framework-general-model-serializer/
        fields = '__all__'
        depth = 3
    
    def __init__(self, instance=None, *args, **kwargs):
        
        super(ConfigSerializer, self).__init__(*args, **kwargs)
        kind = type(instance)
        if kind == QuerySet or kind == list: # the first argument may be a list/queryset instead of a single object to serialize
            kind = type(instance[0])
        self.Meta.model = kind
        
    def get_blocks(self, obj):
        serializer = BlockSerializer(obj.get_all_blocks(), many=True)
        return serializer.data
