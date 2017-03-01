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

def get_type(filepath):
    """
    Simple function used to classify a file into web-dev related categories depending on the extension of its pathname
    """
    
    image_ext = ('.jpeg','.jpg', '.tiff', '.gif', '.bmp', '.png', '.svg')
    audio_ext = ('.mp3', '.wav', '.ogg', '.m4a')
    video_ext = ('.mp4')
    
    extension = os.path.splitext(filepath)[1]
    if extension.lower() == ".js":
        return 'js'
    elif extension.lower() == '.css':
        return 'css'
    elif extension.lower() in image_ext:
        return 'image'
    elif extension.lower() in audio_ext:
        return 'audio'
    elif extension.lower() in video_ext:
        return 'video'
    else :
        return 'other'
    
    
