from django.db import models

from Users.models import CustomUser


class Achievement(models.Model):
    name = models.CharField(max_length=16, primary_key=True)


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
    achievement = models.ForeignKey(Achievement, related_name='levels', on_delete=models.CASCADE)


class AchievementProgress(models.Model):
    achievement = models.ForeignKey(Achievement, related_name='progress', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='achievements', on_delete=models.CASCADE)
    last_achieved_level = models.IntegerField(default=0)
    current_value = models.IntegerField(default=0)
    is_achieved = models.BooleanField(default=False)
    is_redeemed = models.BooleanField(default=False)

    class Meta:
        unique_together = (('achievement', 'user'),)
