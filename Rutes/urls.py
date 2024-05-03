from django.contrib import admin
from django.urls import path

from Rutes import views

urlpatterns = [
    path('rutes/', views.rutesApi, name='rutesApi'),
    path('addruta/', views.afegirRuta, name='afegirRuta'),
    #path('punts/', views.puntsApi, name='puntsApi'),
    path('puntsInterRuta/', views.AfegirPuntRuta, name='puntsIntermedisApi'),
    path('routes/<int:rute_id>/puntos-intermedios/', views.punts_intermedis_list, name='puntos_intermedios'),
    path('routes/completed-routes/', views.completed_routes_view, name='completed-routes'),
    path('routes/<int:rute_id>/average-rating/', views.average_rating, name='average_rating'),
    path('routes/<int:rute_id>/comments/', views.get_route_comments, name='get_route_comments'),
    path('routes/<int:rute_id>/comment/', views.comment_route, name='comment_route'),
    path('routes/<int:rute_id>/rank/', views.rank_route, name='rank_route'),
    path('routes/<int:rute_id>/completed/', views.ruta_completada, name='complete_route'),
    path('routes/punt_visitat/', views.punts_visitats, name='punts_visitats'),
    path('routes/add_punt_visitat/', views.add_punts_visitats, name='punts_visitats_ruta'),
    path('routes/', views.get_routes, name='get_routes'),
]
