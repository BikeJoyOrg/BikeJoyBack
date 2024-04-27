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

import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def register(request):
    form = CustomUserCreationForm(request.POST)
    username = request.POST['username']
    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success register'}, status=200)
    else:
        return Response({'error': form.errors}, status=400)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method != 'POST':
        return Response({'error': 'Only POST requests are allowed'}, status=400)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    user.save()
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'status': 'success login',
            'token': token.key,
            'user': {
                'username': user.username,
                'coins': user.coins,
                'distance': user.distance,
                'xp': user.xp,
            }
        }, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)


@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    logger.debug("entro a logout_view")
    auth_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
    logger.debug(request.META.get('HTTP_AUTHORIZATION', '').split(' '))
    logger.debug(request.headers.get('Authorization'))
    if not auth_token:
        return Response({'error': 'No token provided'}, status=400)

    try:
        token = Token.objects.get(key=auth_token)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=400)

    User = get_user_model()
    try:
        user = User.objects.get(id=token.user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=400)

    # Delete the token
    token.delete()

    # Logout the user
    logout(request)

    return Response(200)


@api_view(['GET'])
def get_user(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    user_data = {
        'username': user.username,
        'coins': user.coins,
        'distance': user.distance,
        'xp': user.xp,
    }

    return Response(user_data, status=200)
