from django.urls import path
from . import views
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_list'),
    path('api/my-likes/', views.get_my_likes, name='get_my_likes'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]