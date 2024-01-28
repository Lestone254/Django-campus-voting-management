from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
path('', index, name='index'),
path('logout/', out, name='logout'),
path('login', enter, name='enter'),
path('profile/', profile, name='profile'),
path('change/', change, name='change'),
path('audit/', useraudit, name='audit'),
path('vote/', vote, name='vote'),
path('sendotp/', sendotp, name='sendotp'),
path('checkotp/', checkotp, name='checkotp'),
path('receivedata/', receivedata, name='receivedata'),
path('results/', userresults, name='userresults'),
path('update/', update, name='update'),
path('logout/', out, name='logout'),
path("createuser", createadmin, name="createuser")
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)