from django.urls import path
from Items import views

urlpatterns = [
    path('items/', views.list_items, name='item-list'),
    path('items/purchase/<int:item_id>/', views.purchase_item, name='item-purchase'),
]