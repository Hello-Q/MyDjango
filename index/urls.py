from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index1),
    path('<int:id>.html', views.model_index)

]
