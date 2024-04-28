from django.contrib import admin
from django.urls import path

from Rutes import views
from Rutes.views import completed_routes_view, average_rating

urlpatterns = [
    path('rutes/', views.rutesApi, name='rutesApi'),
    #path('punts/', views.puntsApi, name='puntsApi'),
    path('puntsInterRuta/', views.AfegirPuntRuta, name='puntsIntermedisApi'),
    path('puntos-intermedios/<int:rute_id>/', views.punts_intermedis_list, name='puntos_intermedios'),
    path('api/completed-routes/', completed_routes_view, name='completed-routes'),
    path('routes/<int:rute_id>/average-rating/', average_rating, name='average_rating'),
]
