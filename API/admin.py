from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Asignatura)
admin.site.register(Sede)
admin.site.register(Sala)
admin.site.register(Docente)
admin.site.register(Estudiante)
admin.site.register(Horario)
admin.site.register(Clase)
admin.site.register(Seccion)