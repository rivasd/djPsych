'''
Created on Feb 28, 2016

@author: Daniel Rivas
'''

def sort_trials(data):
    bulks = {}
    for trial in data:
        type = trial['trial_type']
        if type in bulks:
            # add this trial to the list
            bulks[type].append(trial)
        else:
            bulks[type] = [trial]
            
    return bulks