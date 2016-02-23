'''
Created on Feb 23, 2016

@author: User
'''

from djcollect.models import Participation
from djsend.models import SimCatGlobalSetting

class MyParticipation(Participation):
    
    class Meta:
        proxy=True
        
    


PARTICIPATION_PROXY = MyParticipation
GEN_SETTINGS_MODEL = SimCatGlobalSetting