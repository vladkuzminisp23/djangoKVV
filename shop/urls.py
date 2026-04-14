from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # Новая строка
    path('register/', views.register, name='register'),
    path('game/', views.fish_game, name='fish_game'),
    path('save_score/', views.save_score, name='save_score'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
]