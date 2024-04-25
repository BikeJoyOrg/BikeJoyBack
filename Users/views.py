from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from .forms import CustomUserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        username = request.POST['username']
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'errors': 'Username already exists'})
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success register'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'errors': 'Only POST method allowed'})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user.save()
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'status': 'success login', 'token': token.key, 'user': user.username})
        else:
            return JsonResponse({'status': 'error', 'errors': 'Invalid username or password'})
    return JsonResponse({'status': 'error', 'errors': 'Only POST method allowed'})


@csrf_exempt
def logout_view(request):
    auth_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
    print(auth_token)
    if not auth_token:
        return JsonResponse({'status': 'error', 'errors': 'No token provided'})

    try:
        token = Token.objects.get(key=auth_token)
    except Token.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': 'Invalid token'})

    User = get_user_model()
    try:
        user = User.objects.get(id=token.user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': 'User not found'})

    # Delete the token
    token.delete()

    # Logout the user
    logout(request)

    return JsonResponse({'status': 'success logout'})

# Create your views here.
