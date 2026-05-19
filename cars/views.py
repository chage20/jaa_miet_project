from django.shortcuts import render
from .models import Car, CarLike
from django.http import JsonResponse
from .models import CarLike


def cars_list(request):
    cars = Car.objects.all()
    liked_ids = []

    if request.user.is_authenticated:
        # Получаем ID машин, которые лайкнул текущий пользователь
        liked_ids = list(
            CarLike.objects
            .filter(user=request.user)
            .values_list('car_id', flat=True)
        )

    return render(request, 'cars.html', {
        'cars': cars,
        'liked_ids': liked_ids,
    })


def get_my_likes(request):
    """Возвращает JSON со списком ID лайкнутых машин."""
    if not request.user.is_authenticated:
        return JsonResponse({'liked_ids': []})

    liked_ids = list(CarLike.objects.filter(user=request.user).values_list('car_id', flat=True))
    return JsonResponse({'liked_ids': liked_ids})