from django.urls import path, re_path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.index, name='index'),
    path('ShoppingCar.html/', views.ShoppingCarView, name='ShoppingCar'),
    path('message.html/', views.messageView, name='message'),
    path('pagination/<int:page>.html/', views.paginationView, name='pagination'),
]
