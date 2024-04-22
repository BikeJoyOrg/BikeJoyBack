from django.db import models


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    current_value = models.IntegerField()


class Level(models.Model):
    level = models.IntegerField()
    description = models.TextField()
    value_required = models.IntegerField()
    coin_reward = models.IntegerField()
    pet_reward = models.CharField(max_length=255, null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    is_redeemed = models.BooleanField(default=False)
    achievement = models.ForeignKey(Achievement, related_name='levels', on_delete=models.CASCADE)


