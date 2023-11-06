from django.http import JsonResponse
from django.shortcuts import render
import time
import operation.models as md
from django.db.models import Count
from django.shortcuts import render,redirect
from .form import AddressForm,ManageCuisineForm
from datetime import datetime


# Create your views here.
def store_info(request,store_id):
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == "view_store":
            #获取商铺名称
            cuisine_list = md.CuisineInfo.objects.filter(store_id=store_id)
            username = request.session['username']
            context = {
                'store_id':store_id,
                'username':username,
                "cuisine_list":cuisine_list
            }

            return render(request,"CCDS_django/templates/store_info.html",context)

        button_type = request.GET.get('button_type')
        if button_type == 'place_order':
            # 获取下单信息
            cuisine_ids = []
            temp_cuisine_names = []
            cuisine_quantities = []
            temp_cuisine_prices = []
            for key, value in request.GET.items():
                if key.startswith('cuisine_num_'):
                    cuisine_id = key.split('_')[2]
                    cuisine_ids.append(cuisine_id)
                    cuisine_name = md.CuisineInfo.objects.filter(cuisine_id=cuisine_id).values('cuisine_name')
                    temp_cuisine_names.append(cuisine_name)
                    cuisine_quantities.append(value)
                    price = md.CuisineInfo.objects.filter(cuisine_id=cuisine_id).values('cuisine_price')
                    temp_cuisine_prices.append(price)

            cuisine_names = [cuisine_name[0]['cuisine_name'] for cuisine_name in temp_cuisine_names]
            cuisine_prices = [price[0]['cuisine_price'] for price in temp_cuisine_prices]


            sum_cost = 0
            for i in range(len(cuisine_prices)):
                sum_cost += cuisine_prices[i] * float(cuisine_quantities[i])

            cuisines = zip(cuisine_names, cuisine_prices, cuisine_quantities)
            # 获取用户信息
            username = request.session['username']
            tel = request.session['tel']

            # 获取当前订单类型的最大ID
            prefix = "40"
            max_id = md.OrderInfo.objects.aggregate(max_id=Count('order_id'))
            if max_id['max_id']:
                order_id = int(max_id['max_id']) + 1
            else:
                order_id = int(prefix + "0001")

            payment_time = datetime.now()
            order_state = "未支付"
            context = {
                'username': username,
                'tel': tel,
                'cuisines': cuisines,
                'sum_cost': sum_cost,
                'payment_time': payment_time,
                'order_id': order_id,
                'order_state': order_state
            }

            request.session['cuisine_ids'] = cuisine_ids
            request.session['cuisine_names'] = cuisine_names
            request.session['cuisine_prices'] = cuisine_prices
            request.session['cuisine_num'] = cuisine_quantities
            request.session['sum_cost'] = sum_cost
            payment_time_string = payment_time.strftime('%Y-%m-%d %H:%M:%S')
            request.session['payment_time'] = payment_time_string
            request.session['order_id'] = order_id
            request.session['order_state'] = order_state

            return render(request, 'CCDS_django/templates/order_info.html', context)

def order_info(request):
    if request.method == "POST":
        #地址
        addressform = AddressForm(request.POST)
        if addressform.is_valid():
            address = addressform.cleaned_data['address']

        order_id = request.session['order_id']
        username = request.session['username']
        payment_time_string = request.session['payment_time']
        payment_time = datetime.strptime(payment_time_string, '%Y-%m-%d %H:%M:%S')
        total_cost = request.session['sum_cost']
        cuisine_names = request.session['cuisine_names']
        cuisine_prices = request.session['cuisine_prices']
        cuisine_quantities = request.session['cuisine_num']
        cuisine_ids = request.session['cuisine_ids']


        customer_info = md.CustomerInfo.objects.get(customer_name = username)

        customer_id = customer_info.customer_id

        payment_mode = '微信支付'

        new_order = md.OrderInfo.objects.create(order_id = order_id, customer_id = customer_id,
                                                payment_time = payment_time,payment_mode=payment_mode,
                                                order_state=1,total_cost = total_cost)
        new_order.save()

        for i in range(len(cuisine_prices)):
              print("是否进入")
              order_context = md.OrderContext.objects.create(order_id = order_id,cuisine_id = cuisine_ids[i],cuisine_num = cuisine_quantities[i])

        customer_info = md.CustomerInfo.objects.get(customer_name=username)
        customer_info.address = address
        customer_info.save()
        message = '下单成功！等待商家接单！'
        print(message)
        return render(request, 'CCDS_django/templates/pay_success.html', locals())

def pay_success(request):
    if request.method == "GET":
        return redirect('customer_info')


def process_order(request):
    if request.method == 'POST':
        username = request.session['username']
        order_id = request.POST.get('order_id')
        new_state = request.POST.get('new_state')
        cuisines = md.CuisineInfo.objects.all()

        # 更新订单状态
        order = md.OrderInfo.objects.get(order_id=order_id)
        order.order_state = new_state
        order.save()

        order_list = md.OrderInfo.objects.all()
        context = {
            'username':username,
            'order_list':order_list,
            'cuisines':cuisines,
            #'order_contexts':order_contexts
        }

        return render(request, 'CCDS_django/templates/process_order.html',context)

    return render(request, 'CCDS_django/templates/process_order.html',locals())


def manage_cuisine(request):
    if request.method == 'POST':
        button_type = request.POST.get('button_type')
        if button_type == 'off_the_shelves':#下架逻辑
            username = request.session['username']
            cuisine_id = request.POST.get('cuisine_id')  # 获取要下架的菜品id

            cuisine = md.CuisineInfo.objects.get(cuisine_id=cuisine_id)  # 根据id获取菜品对象
            cuisine.delete()  # 删除菜品对象
            if md.CuisineInfo.objects.exists():
                cuisine_list = md.CuisineInfo.objects.all()
                context = {
                    'username': username,
                    'cuisine_list': cuisine_list,
                }
                # 执行其他操作
            else:
                context = {
                    'username': username
                }

            return render(request,'CCDS_django/templates/manage_cuisine.html',context)

        elif button_type == 'shelves':#上架逻辑

            manageCuisneForm = ManageCuisineForm(request.POST)
            if manageCuisneForm.is_valid():
                # 获取当前cuisine类型的最大ID
                prefix = "50"
                max_id = md.CuisineInfo.objects.aggregate(max_id=Count('cuisine_id'))
                if max_id['max_id']:
                    cuisine_id = int(max_id['max_id']) + 1
                else:
                    cuisine_id = int(prefix + "0001")

                username = request.session['username']
                cuisine_name = manageCuisneForm.cleaned_data['cuisine_name']
                cuisine_price = manageCuisneForm.cleaned_data['cuisine_price']
                merchant = md.MerchatInfo.objects.get(merchant_name = username)
                merchant_id = merchant.merchant_id

                store_ids = md.StoreInfo.objects.filter(merchant__merchant_id=merchant_id).values_list('store_id',
                                                                                                    flat=True)
                store_ids = list(store_ids)

                #将新增菜品存入数据库
                new_cuisine= md.CuisineInfo.objects.create(cuisine_id = cuisine_id,
                                                           store_id = store_ids[0],
                                                            cuisine_name = cuisine_name,
                                                            cuisine_price = cuisine_price)

                if md.CuisineInfo.objects.exists():
                    cuisine_list = md.CuisineInfo.objects.all()
                    context = {
                        'username': username,
                        'cuisine_list': cuisine_list,
                    }

                else:
                    context = {
                        'username': username
                    }

                return render(request,'CCDS_django/templates/manage_cuisine.html',context)







