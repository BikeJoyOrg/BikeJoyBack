from django.db import models

# Create your models here.

class Facultades(models.Model):
    FacultadId = models.AutoField(primary_key=True)
    FacultadNombre = models.CharField(max_length=50)

class Alumnos(models.Model):
    AlumnoId = models.AutoField(primary_key=True)
    AlumnoNombre = models.CharField(max_length=50)
    AlumnoPrograma = models.CharField(max_length=50)    
    FechaDeIngreso = models.DateField()
    


