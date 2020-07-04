"""
WSGI config for django_school project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
import site
site.addsitedir('/root/Desktop/testdjangoschool/lib/python3.7/site-packages')

import sys
sys.path.append('/root/Desktop/testdjangoschool/src/django_school/django_school')


sys.path.append('/root/Desktop/testdjangoschool/src/django_school')


from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_school.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_school.settings'

application = get_wsgi_application()


# ===================== /root/Desktop/testdjangoschool
# wsgi.py file begin 
'''
import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('/root/Desktop/testdjangoschool/src/django_school')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/root/Desktop/testdjangoschool/Lib/site-packages')

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_school.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# wsgi.py file end
'''
# ===================



