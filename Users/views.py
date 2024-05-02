from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUser
from .forms import CustomUserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from Achievements.models import Achievement, AchievementProgress

@csrf_exempt
@api_view(['POST'])
def register(request):
    form = CustomUserCreationForm(request.POST)
    username = request.POST['username']
    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    if form.is_valid():
        user = form.save()

        # Crear una instancia de AchievementProgress para cada Achievement
        for achievement in Achievement.objects.all():
            AchievementProgress.objects.create(achievement=achievement, user=user)
        return Response(status=200)
    else:
        return Response({'error': form.errors}, status=400)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    user.save()
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'coins': user.coins,
                'distance': user.distance,
                'xp': user.xp,
                'monthlyDistance': user.monthlyDistance,
                'weeklyDistance': user.weeklyDistance,
                'dailyDistance': user.dailyDistance,
            }
        }, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = request.auth
    # Delete the token
    token.delete()

    # Logout the user
    logout(request)

    return Response(200)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user

    user_data = {
        'user': {
            'username': user.username,
            'coins': user.coins,
            'distance': user.distance,
            'xp': user.xp,
            'monthlyDistance': user.monthlyDistance,
            'weeklyDistance': user.weeklyDistance,
            'dailyDistance': user.dailyDistance,
        }
    }

    return Response(user_data, status=200)


@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualitzar_stats(request):
    user = request.user
    data = request.data
    try:
        user.distance = data['distance']
    except KeyError:
        return JsonResponse({'status': 'error', 'message': 'No se proporcionó la distancia'}, status=400)
    user.save()
    return JsonResponse({'status': 'success update'}, status=200)

@csrf_exempt
@api_view(['GET'])
def get_users(request):
    try:
        users = CustomUser.objects.all()
        users_data = []
        for user in users:
            user_data = {
                'username': user.username,
                'coins': user.coins,
                'distance': user.distance,
                'xp': user.xp,
                'monthlyDistance': user.monthlyDistance,
                'weeklyDistance': user.weeklyDistance,
                'dailyDistance': user.dailyDistance,
            }
            users_data.append(user_data)
        return Response(users_data, status=200)
    except Exception as e:
        return JsonResponse({'message': f'Error al obtener información de usuarios: {str(e)}'}, status=500)