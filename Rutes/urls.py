from django.contrib import admin
from django.urls import path

from Rutes import views

urlpatterns = [
    path('rutes/', views.rutesApi, name='rutesApi'),
    #path('punts/', views.puntsApi, name='puntsApi'),
    path('puntsInterRuta/', views.AfegirPuntRuta, name='puntsIntermedisApi'),
    path('puntos-intermedios/<int:rute_id>/', views.punts_intermedis_list, name='puntos_intermedios'),
]
