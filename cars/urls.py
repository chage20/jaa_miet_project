from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_list'),
    # Новый путь для AJAX запроса
    path('api/my-likes/', views.get_my_likes, name='get_my_likes'),
]