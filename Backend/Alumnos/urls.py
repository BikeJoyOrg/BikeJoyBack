from django.urls import path
from Alumnos import views
from django.contrib import admin
from Alumnos.views import lista_facultades



urlpatterns = [
    path('admin/', admin.site.urls),
    path('facultad/', views.facultadesApi),
    path('facultad/<int:id>/', views.facultadesApi, name='facultad-detail'),
    
    path('facultad/agregar/', views.agregar_facultad, name='agregar_facultad'),
    path('facultad/editar/<int:id>/', views.editar_facultad, name='editar_facultad'),

    path('facultad/eliminar/<int:id>/', views.eliminar_facultad, name='eliminar_facultad'),
    path('facultades/', views.facultadesApi, name='facultadesApi'),
    path('lista_facultades/', views.lista_facultades, name='lista_facultades'),


    path('formulario/', views.formulario_facultad, name='formulario_facultad'),

    path('alumno/', views.alumnosApi),
    path('alumno/<int:id>/', views.alumnosApi, name='alumno-detail'),
    
]
