from django.urls import path

from Stations import views

urlpatterns = [
    path('stations/', views.get_info_stations, name='obtener-informacion-estaciones'),
    path('stations/<int:station_id>/', views.get_state_stations, name='obtener-estado-estaciones'),
]
