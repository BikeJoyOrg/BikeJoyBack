from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Achievement, Level, AchievementProgress
from .serializers import AchievementSerializer, AchievementProgressSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_info_achievements_progress(request):
    user = request.user
    try:
        achievements_progress = AchievementProgress.objects.filter(user=user)
        achievements_progress_serializer = AchievementProgressSerializer(achievements_progress, many=True)
        return JsonResponse({'achievementsProgress': achievements_progress_serializer.data}, status=200)

    except Exception as e:
        print(f"Error al obtener información del progreso de los achievements: {e}")
        return JsonResponse(
            {'message': f'Error al obtener información del progreso de los achievements: {str(e)}', 'user': str(user)},
            status=500)


@csrf_exempt
@api_view(['PATCH'])
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
@api_view(['PATCH'])
def update_level_achieved(request, achievement_name, level):
    try:
        new_value = request.data.get('is_achieved')
        level = Level.objects.get(achievement=achievement_name, level=level)
        level.is_achieved = new_value
        level.save()
        return JsonResponse({'message': 'Level achieved status updated successfully'}, status=200)
    except Level.DoesNotExist:
        return JsonResponse({'message': 'Level not found'}, status=404)


@csrf_exempt
@api_view(['PATCH'])
def update_level_redeemed(request, achievement_name, level):
    try:
        new_value = request.data.get('is_redeemed')
        level = Level.objects.get(achievement=achievement_name, level=level)
        level.is_redeemed = new_value
        level.save()
        return JsonResponse({'message': 'Level redeemed status updated successfully'}, status=200)
    except Level.DoesNotExist:
        return JsonResponse({'message': 'Level not found'}, status=404)
