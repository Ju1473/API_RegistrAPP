from django.urls import re_path as url
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api/asignatura/$',AsignaturaViewSet.as_view()),
    url(r'^api/sede/$',SedeViewSet.as_view()),
    url(r'^api/sala/$',SalaViewSet.as_view()),
    url(r'^api/docente/$',DocenteViewSet.as_view()),
    url(r'^api/estudiante/$',EstudianteViewSet.as_view()),
    url(r'^api/horario/$',HorarioViewSet.as_view()),
    url(r'^api/clase/$',ClaseViewSet.as_view()),
    url(r'^api/seccion/$',SeccionViewSet.as_view()),
]

urlpatterns=format_suffix_patterns(urlpatterns)