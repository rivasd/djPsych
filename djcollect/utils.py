'''
Created on Mar 1, 2016

@author: Daniel Rivas
'''
import io
import csv

def get_csv_iostring_from_participation(participation):
    stringfile = io.StringIO(newline='')
    header_list = participation.get_headers()
    datawriter = csv.DictWriter(stringfile, header_list)
    datawriter.writeheader()
    datawriter.writerows(participation.get_data_as_dict_array())
    # stringfile.close() It must not be closed or else we will get a value error when putting its contents to the zipfile
    return stringfile