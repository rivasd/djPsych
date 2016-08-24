'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
import io
import csv

def unpack(participation):
    trials = participation.get_all_trials()
    data_dicts= []
    header_set = set()
    for trial in trials:
        header_set = header_set.union(trial.get_full_field_names())
        data_dicts.append(trial.toDict())
    return list(header_set), data_dicts

def get_csv_iostring_from_participation(participation):
    stringfile = io.StringIO(newline='')
    header_list, data_dicts = unpack(participation)
    datawriter = csv.DictWriter(stringfile, header_list)
    datawriter.writeheader()
    datawriter.writerows(data_dicts)
    # stringfile.close() It must not be closed or else we will get a value error when putting its contents to the zipfile
    return stringfile