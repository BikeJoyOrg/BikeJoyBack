from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import BikeLane
from .serializers import BikeLaneSerializer


@require_http_methods(["GET"])
def get_info_bikelanes(request):
    try:
        bikelanes = BikeLane.objects.all()
        bikelanes_serializer = BikeLaneSerializer(bikelanes, many=True)
        return JsonResponse({'bikelanes': bikelanes_serializer.data}, status=200)

    except Exception as e:
        print(f"Error al obtener información de bikelanes: {e}")
        return JsonResponse({'message': 'Error al obtener información de bikelanes'}, status=500)