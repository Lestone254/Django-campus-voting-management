from django.urls import path
from .views import *


urlpatterns = [
path('', admindash, name='admindash'),
path('addvoter/', addvoter, name='addvoter'),
path('createusers', createusers, name='createusers'),
path('getusers', getusers, name='getusers'),
path('newpost', newpost, name='newpost'),
path('addpost', addpost, name='addpost'),
path('addcon', addcon, name='addcon'),
path('addschool', addschool, name='addschool'),
path('voterlist', voterlist, name='voterlist'),
path('open', openelection, name='open'),
path('close', close, name='close'),
path('csvadd', csvadd, name='csvadd'),
path('complex/', complexp, name='complexp'),
path('pdfvoter', pdfvoter, name='pdfvoter'),
path('election', elections, name='election'),
path('leaders', leaders, name='leaders'),
path('approve', approve, name='approve'),
path('conlist', conlist, name='conlist'),
path('conpdf', conpdf, name='pdfcon'),
path('adminresults', adminresults, name='adminresults'),
]