'''
Created on Feb 27, 2016

@author: Daniel Rivas
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from djuser.models import Subject
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createSubject(sender, instance, created, **kwargs):
    """
    Creates a Subject automatically for each new User that is created. no subclasses, I reaaaaaaaaaally don't want to maintain multiple Subject subclasses
    """
    if created:
        # a new user has been created. we should create an instance of every subclass of expManager.BaseSubject
        record = Subject(user=instance)
        record.save()
