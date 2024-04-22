from rest_framework import serializers
from .models import Level
from .models import Achievement


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['level', 'description', 'value_required', 'coin_reward', 'pet_reward', 'is_achieved', 'is_redeemed']


class AchievementSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = Achievement
        fields = ['name', 'current_value', 'levels']
