from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Agrega tus campos adicionales aquí. Por ejemplo:
    #campo_extra1 = models.CharField(max_length=100, default='valor predeterminado')
    coins = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    monthlyDistance = models.IntegerField(default=0)
    weeklyDistance = models.IntegerField(default=0)
    dailyDistance = models.IntegerField(default=0)
    completed_routes = models.IntegerField(default=0)
    monthlyCompletedRoutes = models.IntegerField(default=0)
    weeklyCompletedRoutes = models.IntegerField(default=0)
    dailyCompletedRoutes = models.IntegerField(default=0)

