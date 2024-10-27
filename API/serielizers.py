from .models import *
from rest_framework import serializers

class AsignaturaSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    uid = serializers.CharField()

class UsuarioSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    p_nombre = serializers.CharField()
    s_nombre = serializers.CharField()
    p_apellido = serializers.CharField()
    s_apellido = serializers.CharField()
    uid = serializers.CharField()

class AsistenciaSerializer(serializers.Serializer):
    asistidas = serializers.IntegerField()
    clases = serializers.ListField(child=serializers.IntegerField())
    faltas = serializers.IntegerField()
    justificadas = serializers.IntegerField()
    usuario = UsuarioSerializer(required=False)
    porcentaje = serializers.FloatField()
    uid = serializers.CharField()

class ClaseSerializer(serializers.Serializer):
    clases = serializers.ListField(child=serializers.CharField())
    clasesTotales = serializers.IntegerField()
    clases_realizadas = serializers.ListField(child=serializers.IntegerField())
    uid = serializers.CharField()

class HorarioSerializer(serializers.Serializer):
    dia = serializers.CharField()
    hora_ini = serializers.CharField()
    hora_ter = serializers.CharField()
    sala = serializers.CharField()
    uid = serializers.CharField()

class SeccionSerializer(serializers.Serializer):
    asignatura = AsignaturaSerializer()
    asistencia = AsistenciaSerializer(required=False)
    asistencias = serializers.ListField(child=AsistenciaSerializer(), required=False)
    clase = ClaseSerializer()
    codigo = serializers.CharField()
    horario = serializers.ListField(child=HorarioSerializer(), required=False)
    profesor = UsuarioSerializer()
    porcentaje = serializers.FloatField(required=False)
    estudiante = UsuarioSerializer(required=False)
    uid = serializers.CharField()

class QRSerializer(serializers.Serializer):
    uid_clase = serializers.CharField()
    uid_seccion = serializers.CharField()