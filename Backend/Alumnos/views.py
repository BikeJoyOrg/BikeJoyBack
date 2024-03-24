from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.urls import reverse

from Alumnos.models import Facultades, Alumnos
from Alumnos.serializers import FacultadesSerializer, AlumnosSerializer

# Vistas de la API

@csrf_exempt
def facultadesApi(request, id=0):
    if request.method == 'GET':
        facultades = Facultades.objects.all()
        facultades_serializer = FacultadesSerializer(facultades, many=True)
        return JsonResponse(facultades_serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        facultades_serializer = FacultadesSerializer(data=data)
        if facultades_serializer.is_valid():
            facultades_serializer.save()
            facultades = Facultades.objects.all()  # Obtener la lista actualizada de facultades
            return render(request, 'lista_facultades.html', {'facultades': facultades})
        return JsonResponse("Error al guardar facultad", safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        facultad = Facultades.objects.get(FacultadId=data['FacultadId'])
        facultades_serializer = FacultadesSerializer(facultad, data=data)
        if facultades_serializer.is_valid():
            facultades_serializer.save()
            facultades = Facultades.objects.all()  # Obtener la lista actualizada de facultades
            return render(request, 'lista_facultades.html', {'facultades': facultades})
        return JsonResponse("Error al actualizar")
    elif request.method == 'DELETE':
        facultad = Facultades.objects.get(FacultadId=id)
        facultad.delete()
        facultades = Facultades.objects.all()  # Obtener la lista actualizada de facultades
        return render(request, 'lista_facultades.html', {'facultades': facultades})


# Vistas del formulario

def formulario_facultad(request):
    if request.method == 'POST':
        data = request.POST
        facultades_serializer = FacultadesSerializer(data=data)
        if facultades_serializer.is_valid():
            facultades_serializer.save()
            return redirect('lista_facultades')
    return render(request, 'formulario.html')

""" def agregar_facultad(request):
    if request.method == 'POST':
        data = request.POST
        facultades_serializer = FacultadesSerializer(data=data)
        if facultades_serializer.is_valid():
            facultades_serializer.save()
            #facultades = Facultades.objects.all()  # Obtener la lista actualizada de facultades
            #return render(request, 'lista_facultades.html', {'facultades': facultades})
            return redirect(reverse('facultadesApi'))
    return render(request, 'formulario.html') """

def agregar_facultad(request):
    if request.method == 'POST':
        data = request.POST
        facultades_serializer = FacultadesSerializer(data=data)
        if facultades_serializer.is_valid():
            facultades_serializer.save()
            return redirect('lista_facultades')  # Redirigir a la vista lista_facultades
        else:
            return JsonResponse(facultades_serializer.errors, status=400)
    else:
        return render(request, 'formulario.html')
    


def lista_facultades(request):
    facultades = Facultades.objects.all()
    return render(request, 'lista_facultades.html', {'facultades': facultades})

def editar_facultad(request, id):
    facultad = Facultades.objects.get(FacultadId=id)
    if request.method == 'POST':
        # Procesar los datos enviados en el formulario de edición
        # Actualizar la facultad con los nuevos valores
        facultad.FacultadNombre = request.POST['nombre']
        facultad.save()
        return redirect('lista_facultades')
    else:
        return render(request, 'editar_facultad.html', {'facultad': facultad})


def eliminar_facultad(request, id):
    facultad = Facultades.objects.get(FacultadId=id)  
    facultad.delete()
    return redirect('lista_facultades')

@csrf_exempt
def alumnosApi(request, id=0):
    if request.method == 'GET':
        alumnos = Alumnos.objects.all()
        alumnos_serializer = AlumnosSerializer(alumnos, many=True)
        return JsonResponse(alumnos_serializer.data, safe=False)
    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            alumnos_serializer = AlumnosSerializer(data=data)
            if alumnos_serializer.is_valid():
                alumnos_serializer.save()
                return JsonResponse("alumno agregado", safe=False)
            return JsonResponse("Error al guardar alumno", safe=False)
        except Exception as e:
            print(str(e))
            return JsonResponse(f"Error al guardar alumno: {str(e)}", safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        alumno = Alumnos.objects.get(AlumnoId=data['AlumnoId'])
        alumnos_serializer = AlumnosSerializer(alumno, data=data)
        if alumnos_serializer.is_valid():
            alumnos_serializer.save()
            return JsonResponse("alumno actualizado", safe=False)
        return JsonResponse("Error al actualizar")
    elif request.method == 'DELETE':
        alumno = Alumnos.objects.get(AlumnoId=id)
        alumno.delete()
        return JsonResponse("alumno eliminado", safe=False)
