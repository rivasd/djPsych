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