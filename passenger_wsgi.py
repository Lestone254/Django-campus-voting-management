import os
import sys
#
## assuming your django settings file is at '/home/hiremobil/mysite/mysite/settings.py'
## and your manage.py is is at '/home/hiremobil/mysite/manage.py'
path = '/home/tsamoite/public_html/apps/voting'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'voting.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
