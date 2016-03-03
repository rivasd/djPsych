'''
Created on Mar 2, 2016

@author: Daniel
'''

def content_type_is_subclass_of(ct, masterclass):
    """
    This simple method is part of a mega hack to limit the choices on ContentType fields
    """
    actual_model = ct.model_class()
    return issubclass(actual_model, masterclass)