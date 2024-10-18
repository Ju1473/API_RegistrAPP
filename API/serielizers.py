from .models import *
from rest_framework import serializers

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asignatura
        fields = '__all__'

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sede
        fields = ['desc_sede']

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sala
        fields = '__all__'

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Docente
        fields = ['p_nombreD','s_nombreD','p_apellidoD','s_apellidoD','correoD']

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Estudiante
        fields = ['p_nombreE','s_nombreE','p_apellidoE','s_apellidoE','correoE','secciones']

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Horario
        fields = ['dia','hora_inicio','hora_termino']

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clase
        fields = ['id_horario','id_sala']

class SeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Seccion
        fields = '__all__'

