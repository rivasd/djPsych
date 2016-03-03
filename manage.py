#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djPsych.settings.dev") #the default shall be dev! we can put prod back in wsgi.py :)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
