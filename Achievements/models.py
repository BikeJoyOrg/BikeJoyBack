from django.db import models


class Achievement(models.Model):
    name = models.CharField(max_length=16, primary_key=True)
    current_value = models.IntegerField(default=0)


class Level(models.Model):
    LEVEL_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
    ]

    level = models.IntegerField(choices=LEVEL_CHOICES)
    description = models.CharField(max_length=58)
    value_required = models.IntegerField()
    coin_reward = models.IntegerField()
    xp_reward = models.IntegerField()
    pet_reward = models.CharField(max_length=255, null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    is_redeemed = models.BooleanField(default=False)
    achievement = models.ForeignKey(Achievement, related_name='levels', on_delete=models.CASCADE)


