from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Achievement
from .serializers import AchievementSerializer


@require_http_methods(["GET"])
def get_info_achievements(request):
    try:
        achievements = Achievement.objects.all()
        achievements_serializer = AchievementSerializer(achievements, many=True)
        return JsonResponse({'achievements': achievements_serializer.data}, status=200)

    except Exception as e:
        print(f"Error al obtener información de achievements: {e}")
        return JsonResponse({'message': 'Error al obtener información de achievements'}, status=500)
