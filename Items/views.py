from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import ItemForm
from .models import Item, ItemPurchased
from .models import CustomUser
from .serializers import ItemSerializer, ItemPurchasedSerializer


@api_view(['GET'])
def list_items(request):
    items = Item.objects.filter(stock_number__gt=0).order_by('-stock_number')
    serializer = ItemSerializer(items, many=True)
    return Response({'items': serializer.data}, status=200)


@api_view(["GET"])
def list_purchased_items(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        purchased_items = ItemPurchased.objects.filter(user=user).order_by('-date_purchased')
        serializer = ItemPurchasedSerializer(purchased_items, many=True)
        return Response({'purchased_items': serializer.data}, status=200)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_item(request, item_id):
    user = request.user
    print(type(request.user))
    try:
        item = Item.objects.get(id=item_id)
        if item.stock_number < 1:
            return Response({'error': 'Item out of stock'}, status=400)
        if user.coins < item.game_currency_price:
            return Response({'error': 'Not enough coins'}, status=400)

        item.stock_number -= 1
        item.save()

        item_purchased = ItemPurchased(item_title=item.title, item_purchased_price=item.game_currency_price, user=user)
        item_purchased.save()

        user.coins -= item.game_currency_price
        user.save()

        return Response(status=200)
    except ObjectDoesNotExist:
        return Response({'error': 'Item not found'}, status=404)
