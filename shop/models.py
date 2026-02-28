from django.db import models
from django.contrib.auth.models import User  # ВОТ ЭТОГО НЕ ХВАТАЛО

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class GameScore(models.Model):
    # Исправил: добавил импорт User и убрал лишнее "on_" в on_delete
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_achieved = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']