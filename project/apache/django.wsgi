import sys
import os
sys.path.append('/opt/sites/appdirectory') 
sys.path.append('/opt/sites/appdirectory/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
