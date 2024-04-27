from django.urls import path
from Achievements.views import get_info_achievements

urlpatterns = [
    path('achievements/', get_info_achievements, name='get_info_achievements'),
]
