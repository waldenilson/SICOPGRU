#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    #sys.path.append('/opt/dev/django/sicop/lib/python2.7/site-packages')
    #sys.path.append('/opt/dev/django/sicop-geoplan/lib/python2.7/site-packages')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
