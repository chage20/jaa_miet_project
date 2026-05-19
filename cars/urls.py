from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_list'),
    path('api/my-likes/', views.get_my_likes, name='get_my_likes'),
]