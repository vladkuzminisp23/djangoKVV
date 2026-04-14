from django.shortcuts import render, get_object_or_404, redirect  # Добавь redirect сюда
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product
from .models import GameScore
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GameScore
from django.db.models import Max # Добавь этот импорт в самый верх файла
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product # Убедись, что модель Product импортирована

# 1. Функция добавления в корзину
def cart_add(request, product_id):
    # Достаем корзину из сессии (или создаем пустую, если её нет)
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    # ID товара переводим в строку, так как сессии Django любят строки
    pid = str(product.id)
    
    if pid in cart:
        cart[pid]['quantity'] += 1 # Если товар уже есть, увеличиваем количество
    else:
        # Если товара нет, добавляем его со всеми данными
        cart[pid] = {
            'quantity': 1, 
            'price': float(product.price), 
            'name': product.name
        }
        
    # Сохраняем обновленную корзину обратно в сессию
    request.session['cart'] = cart
    # После добавления отправляем пользователя на страницу корзины
    return redirect('cart_detail')

# 2. Функция отображения корзины
def cart_detail(request):
    cart = request.session.get('cart', {})
    
    # Считаем общую сумму товаров в корзине
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'total_price': total_price})

# 3. Функция очистки корзины
def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')

@csrf_exempt # Чтобы упростить AJAX-запрос
def save_score(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        score_value = data.get('score', 0)
        
        # Сохраняем результат игрока
        GameScore.objects.create(user=request.user, score=score_value)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def fish_game(request):
    # Группируем по пользователю и находим его лучший результат
    top_scores = GameScore.objects.values('user__username').annotate(
        max_score=Max('score')
    ).order_by('-max_score')[:5] # Берем топ-5 уникальных игроков
    
    return render(request, 'shop/game.html', {'top_scores': top_scores})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
