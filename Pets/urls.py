from django.urls import path

from Pets import views

urlpatterns = [
    path('pets/getMascota/<str:name>/', views.get_mascota, name='get_mascota'),
    path('pets/getMascotas/', views.get_mascotas, name='get_mascotas'),
    path('pets/getMascotasAconseguidesUsuari/', views.get_mascotas_aconseguides_usuari, name='get_mascotas_aconseguides_usuari'),
    path('pets/equiparMascota/<str:name>/', views.equipar_mascota, name='equipar_mascota'),
    path('pets/createMascotaAconseguida/<str:name>/', views.create_mascota_aconseguida, name='get_mascota'),
    path('pets/lvlUp/<str:name>/', views.lvlUp, name='lvlUp'),
]


