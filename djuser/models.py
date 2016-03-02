from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class BaseSubject(models.Model):
    """
    Abstract base model for a registered human subject with it's full profile data
    
    Uses a OnetoOnefied to the base User model that ships with django.
    'User' already has basic contact info and date joined info, so put here fields that are "experimental subject" things like demographics and other
    """
    
    user = models.OneToOneField(User)
    
    class Meta:
        abstract = True
        
    #optional: birthdate of the subject, to calculate age
    birthday = models.DateField(blank=True, null=True)
    
    #optional: sex of the subject. later, add ugettext_lazy() to translate the choices, don't forget!
    gender_choices = (
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other'),
    )
    sex = models.CharField(choices=gender_choices, max_length=1, blank=True, null=True)
    
    #optional: subject's main occupation
    occupation_choices= (
        ('ft-student', 'full-time student'),
        ('ft-work', 'full-time work'),
        ('pt-student&work', 'part-time student & part-time work'),
        ('ft-student&pt-work', 'full-time student & part-time work'),
    )
    occupation = models.CharField(max_length=32, choices=occupation_choices, blank=True, null=True)
    
    #optional: years of schooling
    years_of_schooling = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class Subject(BaseSubject):
    pass

class profileEntry(model.models):
    pass