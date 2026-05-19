from django.contrib import admin
from .models import Car, CarLike

@admin.register(CarLike)
class CarLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'car__title')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    #  Заменено 'name' → 'title'
    list_display = ('title', 'year', 'price', 'get_likes_count')
    list_filter = ('year',)
    search_fields = ('title',)
    ordering = ('-year',)

    @admin.display(description='Лайки')
    def get_likes_count(self, obj):
        """Динамический подсчёт лайков через обратную связь."""
        return obj.likes.count()