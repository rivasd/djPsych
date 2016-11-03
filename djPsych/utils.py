'''
Created on Mar 4, 2016

@author: Daniel Rivas
'''
import glob 
import os.path
from django.conf import settings


def get_all_js_files_in_exp(exp_label, path=''):
    """
    searches the static directory associated with the experiment exp_label
    and retrieves all javaScript files in the relative path provided
    """
    base_path = settings.BASE_DIR+'/../djexperiments/static/djexperiments/'+exp_label
    files=[]
    for file in glob.glob(os.path.join(base_path, path)+'/*.js'):
        files.append(os.path.basename(file))
    return files
    
def fetch_files_of_type(pathname, ext):
    """
    Searches the pathname relative to the root for this django project for all files that end in the given extension
    """
    if not pathname.endswith("/"):
        pathname = pathname+"/"
    location = os.path.dirname(os.path.join(settings.BASE_DIR, '..', pathname))
    files = []
    for file in glob.glob(location+"/*."+ext):
        files.append(os.path.basename(file))
    
    return files