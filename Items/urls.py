from django.urls import path
from Items import views

urlpatterns = [
    path('items/', views.list_items, name='item-list'),
    path('items/<int:item_id>/purchase/', views.purchase_item, name='item-purchase'),
    path('user/<str:username>/purchases/', views.list_purchased_items, name='purchased-items'),
]