from django.urls import path

from Stations import views

urlpatterns = [
    path('stations/a1', views.charge_info_stations, name='cargar_info_estaciones'),
    path('stations/a2', views.update_stations, name='actualizar-disponibilidad-estaciones'),
    path('stations/a3', views.get_info_stations, name='obtener-informacion-estaciones'),
    path('stations/a4', views.get_state_stations, name='obtener-estado-estaciones'),
    path('stations/a5', views.create_station, name='crear-estacion'),
]
