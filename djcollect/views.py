from django.shortcuts import render
from djexperiments.models import Experiment
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.http.response import HttpResponse
import io
import zipfile
import datetime
from djcollect.utils import get_csv_iostring_from_participation


# Create your views here.
# All of this is meant to be used via fake AJAX downloads using this super plugin: https://github.com/johnculviner/jquery.fileDownload

def create_download_error_resp(error_message):
    return HttpResponse(error_message, content_type='text/html', charset='utf-8')


@login_required
def collect_all(request, exp_label):
    exp = Experiment.objects.prefetch_related('research_group', 'participation_set', 
                                              'participation_set__run_set', 'participation_set__subject').get(label=exp_label)
    if not request.user.groups.filter(name=exp.research_group.name).exists():
        return  create_download_error_resp(_("You do not have permission to view experimental data. Are you logged in as the right user?"))
    
    the_zip = io.BytesIO()
    main_zipfile = zipfile.ZipFile(the_zip, mode='w', compression = zipfile.ZIP_DEFLATED)
    main_zipfile.debug = 3
    
    
    
    
    for participation in exp.participation_set.all():
        
        
        
        name = "subject_"+str(participation.subject.id)+str(participation.started).replace(' ', '_').replace(':', '-')+"diff"
        if participation.parameters is not None:
            name = name+ + str(participation.parameters["difficulty"])
        
        data_as_string_io = get_csv_iostring_from_participation(participation)
        main_zipfile.writestr(name+'.csv', data_as_string_io.getvalue())
        data_as_string_io.close() # Better close it, you never know
    main_zipfile.close()
    # Should be done try to find size of the file?
    
    response = HttpResponse(the_zip.getvalue(), content_type="application/zip, application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="full_data_for_'+exp_label+'_fetched_on_'+str(datetime.date.today())+'.zip"'
    response['Content-Length'] = the_zip.tell()
    return response