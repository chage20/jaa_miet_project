from django.shortcuts import render
from cars.models import Car


def index(request):
    return render(request, 'index.html')


def cars(request):
    cars_list = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars_list})
