'''
Created on Feb 24, 2016

@author: Daniel Rivas
'''

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_markdown.models import MarkdownField


# TODO: maybe reuse this to have intro and outro 'instructions' attached to a global setting?
class Instruction(models.Model):
    """
    This is the sole model for instructions so far, I thought there is not much need for multiple models as I don't see much diversity
    in the kind of fields people may want in an instruction. It supports translation and has a flag for HTML.
    Tell me if you think this is missing something, but I will not be subclassing it, this website is already complicated enough
    
    This does not set the jsPsych cont_key param, until I find a solution to find some kind of ListField that doesnt need the hassle of a ManyToMany rel to keycodes
    """
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    task = GenericForeignKey('content_type', 'object_id') # See: https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/#generic-relations
    text = MarkdownField(help_text=l_('Write your instruction page here using Markdown syntax! see: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet'))
    order = models.PositiveIntegerField(help_text=l_("if a setting has multiple instruction pages, we use this number to sort the order in which you want them presented."))
    after = models.BooleanField(help_text=l_("check if this instruction page is meant to be shown AFTER the task it is attached to."))
    # TODO: switched to Markdown for better editing, but still make sure to disallow HTML sine markdown is a superset of HTML
    
    def toDict(self):
        """
        Kinda serializes this object so that it is ready to be JSON'ed and sent. You could override, still call the parent method and set custom params like cont_key on the returned dict even though
        a direct-from-database solution may be better (sorry!)
        
        In the default only the 'text' and 'is_html' attributes are returned. 
        """
        
        dictionary = {
            'type': 'instructions',
            'text': self.text,
        }
        return dictionary