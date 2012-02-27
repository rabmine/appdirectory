import sys
sys.path += ['', '/opt/python2.6/lib/python2.6/site-packages/setuptools-0.6c11-py2.6.egg', ' /opt/python2.6/lib/python2.6/site-packages/virtualenv-1.7-py2.6.egg', '/opt/pyth on2.6/lib/python26.zip', '/opt/python2.6/lib/python2.6', '/opt/python2.6/lib/pyt hon2.6/plat-linux2', '/opt/python2.6/lib/python2.6/lib-tk', '/opt/python2.6/lib/ python2.6/lib-old', '/opt/python2.6/lib/python2.6/lib-dynload', '/opt/python2.6/ lib/python2.6/site-packages']
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
sys.path.append('/opt/sites/appdirectory') 
sys.path.append('/opt/sites/appdirectory/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
