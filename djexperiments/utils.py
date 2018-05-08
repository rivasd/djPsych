import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_exp_label(label):
    if not re.match( r'^[a-zA-Z0-9][A-Za-z0-9_-]+$', label):
        raise ValidationError(_("Your experiment label must contain only letters, numbers, or underscores"))
