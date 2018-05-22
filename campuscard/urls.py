"""campuscard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import xadmin

from user.views import LoginView, IndexView, ConsumeRecordView, BorrowInfoView, RechargeView, SettingView, PayCodeView
from user.views import UpdatePasswordView, PaymentSetView, PayAuthSetView, TicketView, logout
urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('consume_record/', ConsumeRecordView.as_view(), name='consume_record'),
    path('borrow_info/', BorrowInfoView.as_view(), name='borrow_info'),
    path('recharge/', RechargeView.as_view(), name='recharge'),
    path('setting/', SettingView.as_view(), name='setting'),
    path('paycode/', PayCodeView.as_view(), name='paycode'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
    path('payment_set/', PaymentSetView.as_view(), name='payment_set'),
    path('pay_auth_set/', PayAuthSetView.as_view(), name='pay_auth_set'),
    path('ticket/', TicketView.as_view(), name='ticket'),
    path('logout/', logout, name='logout'),
    path('operation/', include('operation.urls'))

]
