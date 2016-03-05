'''
Created on Mar 4, 2016

@author: Daniel Rivas
'''
import glob 
import os.path


def get_all_js_files_in_exp(path, exp_label):
    """
    searches the static directory associated with the experiment exp_label
    and retrieves all javaScript files in the relative path provided
    """
    base_path = './djexperiments/static/djexperiments/'+exp_label
    files=[]
    