from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from .models import Achievement, Level
from .serializers import AchievementSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def get_info_achievements(request):
    try:
        achievements = Achievement.objects.all()
        achievements_serializer = AchievementSerializer(achievements, many=True)
        return JsonResponse({'achievements': achievements_serializer.data}, status=200)

    except Exception as e:
        print(f"Error al obtener información de achievements: {e}")
        return JsonResponse({'message': 'Error al obtener información de achievements'}, status=500)


@csrf_exempt
@api_view(['POST'])
def update_achievement_value(request, achievement_name):
    try:
        new_value = request.data.get('current_value')
        achievement = Achievement.objects.get(name=achievement_name)
        achievement.current_value = new_value
        achievement.save()
        return JsonResponse({'message': 'Achievement value updated successfully'}, status=200)
    except Achievement.DoesNotExist:
        return JsonResponse({'message': 'Achievement not found'}, status=404)


@csrf_exempt
@api_view(['POST'])
def update_level_achieved(request, level_id):
    try:
        new_value = request.data.get('is_achieved')
        level = Level.objects.get(id=level_id)
        level.is_achieved = new_value
        level.save()
        return JsonResponse({'message': 'Level achieved status updated successfully'}, status=200)
    except Level.DoesNotExist:
        return JsonResponse({'message': 'Level not found'}, status=404)


@csrf_exempt
@api_view(['POST'])
def update_level_redeemed(request, level_id):
    try:
        new_value = request.data.get('is_redeemed')
        level = Level.objects.get(id=level_id)
        level.is_redeemed = new_value
        level.save()
        return JsonResponse({'message': 'Level redeemed status updated successfully'}, status=200)
    except Level.DoesNotExist:
        return JsonResponse({'message': 'Level not found'}, status=404)
