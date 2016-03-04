

from django.db import models
from django.utils.translation import ugettext_lazy as l_
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from djsend.models.CustomGeneral import SimCatGlobalSetting
from djsend.models.BasicBlock import BaseSettingBlock
from django_markdown.models import MarkdownField

class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=16)
    keycode = models.IntegerField(help_text=l_("The character keycode representing the correct response for this category. See: http://www.cambiaresearch.com/articles/15/javascript-key-codes"))
    setting = models.ForeignKey(SimCatGlobalSetting)
    
    def __str__(self):
        return self.name

#TODO:  is there really a point to having an index if everything will be randomized?
class MicroComponentPair(models.Model):
    index = models.PositiveIntegerField()
    setting = models.ForeignKey(SimCatGlobalSetting)
    first = models.CharField(max_length=16)
    second = models.CharField(max_length=16)
    
    def __str__(self):
        return self.setting.name + "-" + str(self.index)

class TextTrial(BaseSettingBlock):
    """
    This model encapsulates a link to a .html django template (or raw html) that lives in the experiment directory
    I could have used a nifty tool like django-forms-builder but I need more than just labels and input, also text.
    
    These form builders are also much too complex and focused on managing and saving data server-side when I just want to show the form and let jsPsych get the value of input fields
    All WYSISWYG editors for html do not support creating forms. So really no choice but raw html here.
    """
    
    #TODO: so this poses a problem for internationalization, figure out later, no time
    text = MarkdownField(help_text=l_("path to your html file inside your experiment directory, probably just its name and extension."))
    cont_btn = models.PositiveSmallIntegerField(null=True, blank=True, help_text=l_("If given, this is the key code a key to advance to the next trial"))
    cont_btn= models.CharField(blank=True, null=True, max_length=24, help_text=l_("The ID of a clickable element in the <form> you just created. When the element is clicked, the trial will advance."))
    
    