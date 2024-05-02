from rest_framework import serializers
from .models import Level, AchievementProgress
from .models import Achievement


class LevelSerializer(serializers.ModelSerializer):
    valueRequired = serializers.IntegerField(source='value_required')
    coinReward = serializers.IntegerField(source='coin_reward')
    xpReward = serializers.IntegerField(source='xp_reward')
    petReward = serializers.CharField(source='pet_reward')

    class Meta:
        model = Level
        fields = ['level', 'description', 'valueRequired', 'coinReward', 'xpReward', 'petReward']


class AchievementSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = Achievement
        fields = ['name', 'levels']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['levels'] = sorted(representation['levels'], key=lambda x: x['level'])
        return representation


class AchievementProgressSerializer(serializers.ModelSerializer):
    lastLevelAchieved = serializers.CharField(source='last_level_achieved')
    currentValue = serializers.CharField(source='current_value')
    isAchieved = serializers.CharField(source='is_achieved')
    isRedeemed = serializers.CharField(source='is_redeemed')

    class Meta:
        model = AchievementProgress
        fields = ['achievement', 'lastLevelAchieved', 'currentValue', 'isAchieved', 'isRedeemed']
