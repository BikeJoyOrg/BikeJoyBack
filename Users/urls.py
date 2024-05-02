from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('getUser/', views.getProfile, name='getProfile'),
    path('updateStats/', views.actualitzar_stats, name='update_user'),
    path('users/getUsers/', views.get_users, name='get_users'),
]