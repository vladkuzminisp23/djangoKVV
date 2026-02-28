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
