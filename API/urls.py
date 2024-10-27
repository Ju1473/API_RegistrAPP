from django.urls import re_path as url, path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api/secciones/$', SeccionesView.as_view()),
    url(r'^api/secciones/(?P<id>[^/]+)/$', SeccionesView.as_view()),
    url(r'^api/qr/$', QRView.as_view()),
    url(r'^api/user/$', UserView.as_view()),
]

urlpatterns=format_suffix_patterns(urlpatterns)