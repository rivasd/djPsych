from .BasicTrials import BaseTrial
from django.db import models



class CogComSimilarityTrial(BaseTrial):
    handles = 'similarity'
    sim_score = models.PositiveIntegerField()
    rt = models.PositiveIntegerField()
    firstStim = models.CharField(max_length=24)
    secondStim = models.CharField(max_length=24)
    kind = models.CharField(max_length=10)
    distance = models.IntegerField()
    
class CogComHTMLTrial(BaseTrial):
    handles = 'html'
    difficulty = models.PositiveIntegerField(null=True)
    ruleFound = models.BooleanField(default=False)
    ruleDescription = models.TextField(null=True)
    stratDescription = models.TextField(null=True)
    
class ABXTrial(BaseTrial):
    handles = 'abx'
    rt = models.IntegerField()
    correct = models.BooleanField(default = False)
    A = models.CharField(max_length=1024, null = True)
    B = models.CharField(max_length=1024, null = True)
    X = models.CharField(max_length=1024, null = True)
    key_press = models.IntegerField(null = True)
    
class AudioABXTrial(BaseTrial):
    handles = 'audio-abx'
    rt = models.IntegerField()
    correct = models.BooleanField(default = False)
    A = models.CharField(max_length=1024, null = True)
    B = models.CharField(max_length=1024, null = True)
    X = models.CharField(max_length=1024, null = True)
    key_press = models.IntegerField(null = True)
    
class relationCategorizationTrial(BaseTrial):
    handles = 'relation-categorization'
    rt = models.IntegerField()
    correct = models.BooleanField(default = False)
    A = models.CharField(max_length=1024, null = True)
    B = models.CharField(max_length=1024, null = True)
    key_press = models.IntegerField(null = True)