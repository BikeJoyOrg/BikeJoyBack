from rest_framework import serializers
from Alumnos.models import Facultades, Alumnos


class FacultadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultades
        fields = ('FacultadId', 'FacultadNombre')

class AlumnosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnos
        fields = ('AlumnoId', 'AlumnoNombre', 'AlumnoPrograma', 'FechaDeIngreso')

