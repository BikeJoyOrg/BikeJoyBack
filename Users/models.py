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


def reset_monthly_distance():
    CustomUser.objects.update(monthlyDistance=0)


def reset_weekly_distance():
    CustomUser.objects.update(weeklyDistance=0)


def reset_daily_distance():
    CustomUser.objects.update(dailyDistance=0)
