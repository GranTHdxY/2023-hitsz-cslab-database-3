from django.urls import path,include
from .views import sign_up,homepage,login_in,customer_info,manager_info,merchant_info

urlpatterns = [
    path('loginin/',login_in, name='loginin'),
    path('signup/', sign_up, name='signup'),
    path('homepage/',homepage, name='homepage'),
    path('manager_info/',manager_info, name='manager_info'),
    path('customer_info/',customer_info, name='customer_info'),
    path('merchant_info/',merchant_info, name='merchant_info'),
    path('order/', include('operation.urls'))
]
