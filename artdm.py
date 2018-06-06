from djexperiments.models import Experiment
from django.contrib.auth.models import User
from djcollect.models import Participation

artdmexp = Experiment.objects.get(label="artdm")

all_subjects = artdmexp.participations.all()

filtered_subject_id = [subj.user.id for subj in all_subjects if subj.experiment_set.count() < 2]

users_to_delete = User.objects.filter(id__in=filtered_subject_id)
users_to_delete.delete()

remaining_parts = Participation.objects.filter(experiment=artdmexp)
remaining_parts.delete()
