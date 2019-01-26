from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView
from .form import *
# Create your views here.


def views(request):
    return HttpResponse('hello')


def mydate(request, year, month, day):
    return HttpResponse(str(year)+'/'+str(month)+'/'+str(day))


def myyear(request, year):
    month = request.GET.get('month')
    return render(request, 'myyear.html', context={'month': month})


def index(request):
    type_list = Product.objects.values('type').distinct()
    name_list = Product.objects.values('name', 'type')
    return render(request, 'index1.html', context=locals(), status=500)


class ProductList(ListView):
    context_object_name = 'type_list'
    template_name = 'index.html'
    queryset = Product.objects.values('type').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_list'] = Product.objects.values('type', 'name')
        # context['type_list'] = Product.objects.values('type')
        return context


class ProductListTest(ListView):
    context_object_name = 'type_list'
    template_name = 'test.html'
    model = Product
    queryset = model.objects.values('type')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Product.objects.values('name')
        context['id'] = Product.objects.values('id')
        return context


def index(request):
    product = ProductForm()
    return render(request, 'data_form.html', context=locals())
