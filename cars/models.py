from django.db import models
from django.conf import settings

class Car(models.Model):
    title = models.CharField('Название', max_length=200)
    price = models.IntegerField('Цена (₽)')
    year = models.IntegerField('Год выпуска')
    engine_volume = models.DecimalField('Объем двигателя (л)', max_digits=3, decimal_places=1, default=2.0)
    image = models.ImageField('Фото', upload_to='cars_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.year})"


class CarLike(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('car', 'user')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f"{self.user.username} → {self.car.title}"