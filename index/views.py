from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView
from .form import *
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.


def views(request):
    return HttpResponse('hello')


def mydate(request, year, month, day):
    return HttpResponse(str(year)+'/'+str(month)+'/'+str(day))


def myyear(request, year):
    month = request.GET.get('month')
    return render(request, 'myyear.html', context={'month': month})


def index1(request):
    type_list = Product.objects.values('type').distinct()
    name_list = Product.objects.values('name', 'type')
    username = request.user.username
    return render(request, 'index.html', context=locals(), status=500)


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


@login_required(login_url='/user/login.html')
@permission_required(perm='index.visit_Product', login_url='/user/findpassword.html')
# @permission_required(perm='index.visit_Product', login_url='/user/login.html')
def index(request):
    # GET请求
    username = request.user.username
    product = request.GET.get('product', '')
    price = request.GET.get('price', '')
    if product:
        # 获取session中的数据，不存在返回空
        product_list = request.session.get('product_info', [])
        # 判断当前请求参数是否存在列表product_list中
        if not product in product_list:
            # 将当前参数加入product_list中
            product_list.append({'price': price, 'product': product})
        # 更新储存在session中的数据
        request.session['product_info'] = product_list
        print(request.session.values())
        return redirect('/')
    return render(request, 'index.html', locals())


@login_required(login_url='/user/login.html')
def ShoppingCarView(request):
    # 获取储存在Session中的数据，不存在返回空列表
    product_list = request.session.get('product_info', [])
    # 获取请求参数，没有返回空
    del_product = request.GET.get('product', '')
    # 判断是否为空，若非空，则删除session中的商品信息
    if del_product:
            # 删除session中的某个商品数据
        for i in product_list:
            if i['product'] == del_product:
                product_list.remove(i)
        # 将删除后的数据更新进session
        request.session['product_list'] = product_list
        return redirect('/')
    return render(request, 'ShoppingCar.html', locals())


@login_required(login_url='/user/login.html')
def index2(request):
    user = request.user
    if user.has_perm('index.visit_Product'):
        return render(request, 'index.html', locals())
    else:
        return redirect('/user/login.html')


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
