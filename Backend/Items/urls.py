from django.urls import path
from Items import views

urlpatterns = [
    path('items/', views.listItems, name='item-list'),
    path('items/purchase/<int:item_id>/', views.purchaseItem, name='item-purchase'),
    path('items/new/', views.createItem, name='item-create'),
]