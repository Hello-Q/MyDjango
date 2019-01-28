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
    # GET请求
    if request.method == 'GET':
        product = ProductForm()
        return render(request, 'data_form.html', context=locals())
    # POST请求
    else:
        product = ProductForm(request.POST)
        if product.is_valid():
            # 获取网页控件name的数据
            name = product['name']
            cname = product.cleaned_data['name']
            print(cname)
            return HttpResponse('提交成功')
        else:
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())


def model_index(request, id):
    if request.method == 'GET':
        instance = Product.objects.filter(id=id)
        if instance:
            product = ProductForm(instance=instance[0])
        else:
            product = ProductForm()
        return render(request, 'data_form.html', locals())
    else:
        product = ProductForm(request.POST)
        if product.is_valid():
            weight = product.cleaned_data['weight']
            product.save()
            return HttpResponse('提交成功')
        else:
            error_msg = product.error.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())
