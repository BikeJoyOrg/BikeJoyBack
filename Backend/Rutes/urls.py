from django.contrib import admin
from django.urls import path

from Rutes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rutes/', views.rutesApi, name='rutesApi'),
    #path('punts/', views.puntsApi, name='puntsApi'),
    path('puntsInterRuta/', views.AfegirPuntRuta, name='puntsIntermedisApi'),
]
