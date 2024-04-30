from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('getUser/', views.get_user, name='get_user'),
    path('updateStats/', views.actualitzar_stats, name='update_user'),
]