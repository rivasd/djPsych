'''
Created on Feb 14, 2016

@author: Daniel
'''

class SettingException(Exception):
    pass
        
class NoAppropriateModel(Exception):
    pass

class PayoutException(Exception):
    pass

class BackendConfigException(Exception):
    pass

class ParticipationRefused(Exception):
    pass