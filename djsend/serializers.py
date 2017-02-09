'''
Created on 6 déc. 2016

@author: Daniel Rivas
'''

from rest_framework import serializers
from django.db.models.query import QuerySet
from django.db import models
from django.contrib.contenttypes.models import ContentType
from djsend.models.BasicGeneral import GenericGlobalSetting
from djsend.models.BasicBlock import GenericSettingBlock
from rest_framework.serializers import ValidationError
from rest_framework.fields import empty
from .models import Instruction, Question



class InstructionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Instruction
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = "__all__"


class TimelineSerializer(serializers.ListSerializer):
    
    
    def to_representation(self, data):
        """"
        We override the to_representation method because each object in the data will be an instance of a different model
        We cannot possibly use the same Serializer to handle all of them, so we instantiate one each time !
        """
        iterable = data.all() if isinstance(data, models.Manager) else data
        serialized_timeline = []
        for item in iterable:
            # before we serialize each object with our generic blockSerializer, check if the model specifies a custom serializer to use
            # useful for complex jsPsych blocks
     
            block_serializer = getattr(item, "serializer_class", False)
            if block_serializer:
                serialized_timeline.append(block_serializer(item).to_representation(item))
            else:
                serialized_timeline.append(type(self.child)(item).to_representation(item)) # if the model does not have a "serializer_class", then use the generic one
        return serialized_timeline

    
class BlockSerializer(serializers.ModelSerializer):
    """
    Another generic modelSerializers, meant for block models
    """ 
    
    content_type = serializers.SerializerMethodField(read_only = True)
    instructions = InstructionSerializer(many=True)
    questions = QuestionSerializer(many = True)
    
    class Meta:
        model = GenericSettingBlock
        exclude = ('save_with','global_settings_type', 'global_settings_id')
        list_serializer_class = TimelineSerializer
    
    def __init__(self, instance=None, *args, **kwargs):
        
        model = kwargs.pop('model', None)
        super(BlockSerializer, self).__init__(instance, *args, **kwargs)
        kind = type(instance)
        if model is not None:
            kind = model
        elif kind == QuerySet or kind == list: # We have a queryset of model instances or a list of model instances
            kind = type(instance[0])
        elif instance is None:
            kind = self.Meta.model
        
            
        
        self.Meta.model = kind

    def get_content_type(self, obj):
        """
        The method used to populate the 'content_type' member on the serialized block
        Is simply the id of the ContentType of this object's model, needed when updating to query the right django Model that created that block
        """
        
        return ContentType.objects.get_for_model(obj).id

    
    def validate_content_type(self, data):
        """
        A hacky way to ensure all data dicts that try to represent blocks have the a 'content-type' key,
        since django rest framework won't let me set a field as both 'required' and 'read-only' (go figure...)
        """
        if data is empty:
            raise ValidationError("the type of the block must be specified")
        return data
    
    def to_internal_value(self, data):
        
        # make sure 
        return serializers.ModelSerializer.to_internal_value(self, data)
    
    
class TimelineField(serializers.ListField):
    
    child = BlockSerializer()
    
    def to_internal_value(self, data):
        return serializers.ListField.to_internal_value(self, data)

    
    def to_representation(self, data):
        return serializers.ListField.to_representation(self, data)

class ConfigSerializer(serializers.ModelSerializer):
    """
    Generic serializer for experimental configuration.
    A ModelSerializer but whose model is not set in advance, you need to assign it at object instatiation time
    
    """
    
    content_type = serializers.SerializerMethodField(read_only=True)
    timeline = BlockSerializer(many=True, source="get_all_blocks")
    
    class Meta:
        model = GenericGlobalSetting # the model is left unspecified, you must specify it when instatiating the serializer, see: https://blog.hipwerk.com/django-rest-framework-general-model-serializer/
        exclude = ('experiment',)
        
    
    def __init__(self, instance=None, *args, **kwargs):
        
        super(ConfigSerializer, self).__init__(instance, *args, **kwargs)
        kind = type(instance)
        if kind == QuerySet or kind == list: # the first argument may be a list/queryset instead of a single object to serialize
            kind = type(instance[0])
            
        if instance is not None:
            self.Meta.model = kind
        
    def get_blocks(self, obj):
        return obj.get_all_blocks()
    
    def get_content_type(self, obj):
        """
        The method used to populate the 'content_type' member on the serialized block
        Is simply the id of the ContentType of this object's model, needed when updating to query the right django Model that created that block
        """
        
    
        return ContentType.objects.get_for_model(obj).id
    
    def update(self, instance, validated_data):
        return serializers.ModelSerializer.update(self, instance, validated_data)
    
    def to_internal_value(self, data):
        return serializers.ModelSerializer.to_internal_value(self, data)
    