from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ItemForm
from .models import Item, ItemPurchased
from .serializers import ItemSerializer


@api_view(['GET'])
def list_items(request):
    items = Item.objects.filter(stock_number__gt=0)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def purchase_item(request, item_id):
    if request.user.is_authenticated:
        try:
            item = Item.objects.get(id=item_id)
            if item.stock_number < 1:
                return Response({'error': 'Item out of stock'}, status=400)
            item.stock_number -= 1
            item.save()

            item_purchased = ItemPurchased(item=item, user=request.user)
            item_purchased.save()

            return Response(status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'Item not found'}, status=404)
    else:
        return Response({'error': 'User not authenticated'}, status=401)


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item-list')
        else:
            print(form.errors)
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form, 'is_edit': False})


def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item-list')
        else:
            print(form.errors)
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form, 'is_edit': False, 'item': item})
