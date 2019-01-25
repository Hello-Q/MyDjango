from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.views),
    # path('<year>/<int:month>/<slug:day>', views.mydate),
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})', views.mydate),
    re_path('(?P<year>[0-9]{4}).html', views.myyear, name='myyear'),
    path('', views.index),
    path('index', views.ProductList.as_view()),
    path('test/', views.ProductListTest.as_view())
]
