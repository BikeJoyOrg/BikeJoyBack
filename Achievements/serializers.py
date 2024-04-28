from rest_framework import serializers
from .models import Level
from .models import Achievement


class LevelSerializer(serializers.ModelSerializer):
    valueRequired = serializers.IntegerField(source='value_required')
    coinReward = serializers.IntegerField(source='coin_reward')
    xpReward = serializers.IntegerField(source='xp_reward')
    petReward = serializers.CharField(source='pet_reward')
    isAchieved = serializers.BooleanField(source='is_achieved')
    isRedeemed = serializers.BooleanField(source='is_redeemed')

    class Meta:
        model = Level
        fields = ['level', 'description', 'valueRequired', 'coinReward', 'xpReward', 'petReward', 'isAchieved', 'isRedeemed']


class AchievementSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)
    currentValue = serializers.IntegerField(source='current_value')

    class Meta:
        model = Achievement
        fields = ['name', 'currentValue', 'levels']
