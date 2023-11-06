from django.shortcuts import render,redirect
import user.form as form
import user.models as md
from django.contrib import messages
from django.db.models import Count, Q

# Create your views here.
def homepage(request):
    if request.method == "GET":
        button_type = request.GET.get('button_type')
        if button_type == 'loginin':
            # 登录逻辑
            return render(request, 'CCDS_django/templates/login_in.html', locals())
        elif button_type == 'signup':
            # 注册逻辑
            return render(request, 'CCDS_django/templates/sign_up.html', locals())

    return render(request, 'CCDS_django/templates/homepage.html')

def sign_up(request):
    signup_form = form.SignupForm()
    if request.method == "POST":
        signup_form = form.SignupForm(request.POST)
        #print(signup_form.errors)
        if signup_form.is_valid():  # 获取数据
            username = signup_form.cleaned_data['username']
            password1 = signup_form.cleaned_data['password1']
            password2 = signup_form.cleaned_data['password2']
            tel = signup_form.cleaned_data['tel']
            user_type_mapping = {
                '1': '顾客',  # 顾客
                '2': '商家',  # 商家
                '3': '食堂管理员',  # 食堂管理员
            }
            usertype = user_type_mapping[signup_form.cleaned_data['usertype']]

            if password1 != password2:  # 判断两次密码是否相同
                message = '两次密码不同'
                print(message)
                return render(request, 'CCDS_django/templates/sign_up.html', locals())
            else:
                if md.UserInfo.objects.filter(username = username).exists():  #用户名已经存在于数据库中
                    message = '用户名已经存在~请换一个'
                    print(message)
                    return render(request, 'CCDS_django/templates/sign_up.html', locals())
                # 当一切都OK的情况下，创建新用户
                else:
                    # 获取当前用户类型的最大ID
                    prefix = ""
                    if usertype == '顾客':
                        prefix = "10"
                        max_id = md.UserInfo.objects.filter(user_type=usertype).aggregate(max_id=Count('customer_id'))
                    elif usertype == '商家':
                        prefix = "20"
                        max_id = md.UserInfo.objects.filter(user_type=usertype).aggregate(max_id=Count('merchant_id'))
                    elif usertype == '食堂管理员':
                        prefix = "30"
                        max_id = md.UserInfo.objects.filter(user_type=usertype).aggregate(max_id=Count('manager_id'))

                    if max_id['max_id']:
                        new_id = int(max_id['max_id']) + 1
                    else:
                        new_id = int(prefix + "0001")

                    new_cus = md.UserInfo.objects.create(username=username,password=password1, user_tel=tel, user_type= usertype)
                    new_cus.save()
                    # 根据用户类型，在对应的表中存储用户信息并为其自动编号
                    if usertype == '顾客':
                        # 创建顾客信息
                        new_customer = md.CustomerInfo.objects.create(customer_id = new_id,customer_name=username,phone_number = tel)
                        new_customer.save()
                    elif usertype == '商家':
                        # 创建商家信息
                        new_merchant = md.MerchatInfo.objects.create(merchant_id = new_id,merchant_name = username,merchant_tel = tel)
                        new_merchant.save()
                    elif usertype == '食堂管理员':
                        # 创建食堂管理员信息
                        new_manager = md.ManagerInfo.objects.create(manager_id = new_id,manager_name=username,manager_tel = tel)
                        new_manager.save()

                    # 自动跳转到登录页面
                    login_form = form.LoginForm()
                    message = "注册成功！"
                    print(message)
                    return render(request, 'CCDS_django/templates/login_in.html', locals())  # 自动跳转到登录页面

    return render(request, 'CCDS_django/templates/sign_up.html', {'signup_form': signup_form})

def login_in(request):
    login_form = form.LoginForm()
    if request.method == "GET":
        login_form = form.LoginForm(request.GET)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            print("[DEBUG][GET][LOGIN][username]:{}".format(username))
            print("[DEBUG][GET][LOGIN][password]:{}".format(password))

            try:
                print("[DEBUG][POST][STATE]:查询顾客用户数据库")
                user_cus = md.UserInfo.objects.get(username = username)
                if user_cus.password == password:
                    request.session['username'] = user_cus.username
                    request.session['tel'] = int(user_cus.user_tel)
                    print("[DEBUG][POST][USERNAME]:{}".format(user_cus.username))
                    print("[DEBUG][POST][STATE]:登录成功")
                    messages.success(request, '{}登录成功！'.format(user_cus.username))
                    user_cus.status = 1
                    user_cus.save()
                    if user_cus.user_type == '顾客':
                        return redirect('customer_info')
                    elif user_cus.user_type == '商家':
                        return redirect('merchant_info')
                    elif user_cus.user_type == '食堂管理员':
                        return redirect('manager_info')
                else:
                    print("[DEBUG][POST][STATE]:密码不正确")
                    message = "密码不正确"
            except md.UserInfo.DoesNotExist:
                print("[DEBUG][POST][STATE]:用户不存在")
                message = "用户不存在"

    return render(request, 'CCDS_django/templates/login_in.html', locals())

def manager_info(request):
    username = request.session['username']
    user_info = md.UserInfo.objects.get(username=username)
    # 获取头像数据
    avatar_url = user_info.avatar
    # 获取管理员管理的食堂列表
    manager_info = md.ManagerInfo.objects.filter(manager_name=username)
    canteen_list = [info.canteen.canteen_name for info in manager_info if info.canteen]
    context = {
        'avatar_url': avatar_url,
        'canteen_list': canteen_list,
        'username': username
    }
    return render(request, 'CCDS_django/templates/manager_info.html', context)

def customer_info(request):
    username = request.session['username']
    store_list = md.StoreInfo.objects.all()
    context = {
        'username': username,
        'store_list': store_list,
    }

    if request.method == "GET":
        button_type = request.GET.get('button_type')
        if button_type == 'homepage':
            return render(request, 'CCDS_django/templates/homepage.html', locals())
        elif button_type == 'order_list':
            return render(request, 'CCDS_django/templates/order_info.html', locals())

    return render(request, 'CCDS_django/templates/customer_info.html', context)

def merchant_info(request):
    username = request.session['username']
    store_info = md.StoreInfo.objects.filter(merchant__merchant_name = username)
    store_lists = [store.store_name for store in store_info]
    context = {
        'username': username,
        'store_list': store_lists
    }

    if request.method == "GET":
        button_type = request.GET.get('button_type')

        if button_type == 'process_order':
            username = request.session['username']
            order_list = md.OrderInfo.objects.all()
            cuisines = md.CuisineInfo.objects.all()
            context = {
                'username': username,
                'order_list': order_list,
                'cuisines':cuisines
            }

            return render(request, 'CCDS_django/templates/process_order.html',context)

        elif button_type == 'manage_cuisine':
            username = request.session['username']
            cuisine_list = md.CuisineInfo.objects.all()
            context = {
                'username': username,
                'cuisine_list': cuisine_list,
            }
            return render(request,'CCDS_django/templates/manage_cuisine.html',context)

    return render(request, 'CCDS_django/templates/merchant_info.html', context)









