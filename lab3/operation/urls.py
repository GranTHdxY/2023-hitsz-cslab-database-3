from django.urls import path
from .views import order_info,store_info,pay_success,process_order,manage_cuisine

urlpatterns = [
    path('order_info',order_info, name='order_info'),
    path('pay_success',pay_success,name = 'pay_success'),
    path('process_order',process_order,name = 'process_order'),
    path('manage_cuisine',manage_cuisine,name = 'manage_cuisine'),

    path('store_info/<int:store_id>/',store_info, name='store_info')

]