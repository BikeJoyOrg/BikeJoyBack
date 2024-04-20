from django.urls import path
from BikeLanes.views import get_info_bikelanes

urlpatterns = [
    path('bikelanes/', get_info_bikelanes, name='get_info_bikelanes'),
]