from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название изделия")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Фото товара")
    created_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return self.name