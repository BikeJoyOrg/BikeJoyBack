from django.urls import path
from .views import get_info_achievements, update_achievement_value, update_level_achieved, update_level_redeemed

urlpatterns = [
    path('achievements/', get_info_achievements, name='get_info_achievements'),
    path('achievements/<str:achievement_name>/update_value/', update_achievement_value, name='update_achievement_value'),
    path('achievements/<str:achievement_name>/levels/<int:level>/update_achieved/', update_level_achieved, name='update_level_achieved'),
    path('achievements/<str:achievement_name>/levels/<int:level>/update_redeemed/', update_level_redeemed, name='update_level_redeemed'),
]