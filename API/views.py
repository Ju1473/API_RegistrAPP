from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serielizers import *

# Create your views here.
class AsignaturaViewSet(generics.ListCreateAPIView):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer

class SedeViewSet(generics.ListCreateAPIView):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer

class SalaViewSet(generics.ListCreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

class DocenteViewSet(generics.ListCreateAPIView):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

class EstudianteViewSet(generics.ListCreateAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class HorarioViewSet(generics.ListCreateAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class ClaseViewSet(generics.ListCreateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

class SeccionViewSet(generics.ListCreateAPIView):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

