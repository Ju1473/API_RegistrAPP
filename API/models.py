from django.db import models

# Create your models here.
class Asignatura(models.Model):
    cod_asig=models.CharField(primary_key=True, max_length=30)
    desc_asig=models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.desc_asig
    

class Sede(models.Model):
    id_sede=models.AutoField(primary_key=True)
    desc_sede=models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.desc_sede
    
class Sala(models.Model):
    cod_sala=models.CharField(primary_key=True, max_length=10)
    id_sede=models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cod_sala
    

class Docente(models.Model):
    id_docente=models.AutoField(primary_key=True)
    p_nombreD=models.CharField(max_length=30, null=False)
    s_nombreD=models.CharField(max_length=30, blank=True)
    p_apellidoD=models.CharField(max_length=30, null=False)
    s_apellidoD=models.CharField(max_length=30, blank=True)
    correoD=models.EmailField(unique=True)

    def __str__(self):
        return self.id_docente + ' - ' + self.p_nombreD + ' ' + self.p_apellidoD
    

class Estudiante(models.Model):
    id_estudiante=models.AutoField(primary_key=True)
    p_nombreE=models.CharField(max_length=30, null=False)
    s_nombreE=models.CharField(max_length=30, blank=True)
    p_apellidoE=models.CharField(max_length=30, null=False)
    s_apellidoE=models.CharField(max_length=30, blank=True)
    correoE=models.EmailField(unique=True)
    secciones=models.JSONField()

    def __str__(self):
        return self.id_estudiante + ' - ' + self.p_nombreE + ' ' + self.p_apellidoE
    

class Horario(models.Model):
    id_horario=models.AutoField(primary_key=True)
    dia=models.CharField(max_length=10, null=False)
    hora_inicio=models.TimeField(null=False)
    hora_termino=models.TimeField(null=False)

    def __str__(self):
        return self.id_horario


class Clase(models.Model):
    id_clase=models.AutoField(primary_key=True)
    id_horario=models.ForeignKey(Horario, on_delete=models.CASCADE)
    id_sala=models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_clase


class Seccion(models.Model):
    cod_seccion=models.CharField(primary_key=True, max_length=30)
    cod_asig=models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    id_docente=models.ForeignKey(Docente, on_delete=models.CASCADE)
    id_clases=models.JSONField()
    clases_totales=models.IntegerField()

    def __str__(self):
        return self.cod_seccion