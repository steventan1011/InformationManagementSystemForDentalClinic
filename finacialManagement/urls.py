# -*- coding:utf-8 -*-
# __author__="Liyuanfang"
# __DATE__="2019/5/30"
from django.urls import path
from . import views

app_name = 'finacialManagement'

urlpatterns = [
    path('',views.index,name='index'),
    path('pay/',views.pay,name='pay'),
    path('HrForMF/',views.HrForMF,name='HrForMF'),
    path('HrForMF/api/getHRInfo',views.getHRInfo,name='getHRInfo'),
    path('HrForMF/api/updateHRInfo',views.updateHRInfo,name='updateHRInfo'),
    path('pay/api/getdrugPayment',views.getdrugPayment,name='getdrugPayment'),
    path('pay/api/updatedrugPayment',views.updatedrugPayment,name='updatedrugPayment'),
    path('pay/api/getcheckPayment',views.getcheckPayment,name='getcheckPayment'),
    path('pay/api/updatecheckPayment',views.updatecheckPayment,name='updatecheckPayment')
]