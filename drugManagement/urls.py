# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/5/23"
from django.urls import path, re_path
from django.conf.urls import url, include

from . import views

app_name = 'drugManagement'

urlpatterns = [
    path('',views.index,name='index'),
    path('drug/',views.drug,name='drug'),
    path('HrForMF/',views.hr,name='hr'),
    path('drug/api/getDrugBill',views.getDrugBill,name='getDrugBill'),
    path('drug/api/updateDrugBill',views.updateDrugBill,name='updateDrugBill'),
    path('HrForMF/api/getHRInfo',views.getHRInfo,name='getHRInfo'),
    path('HrForMF/api/updateHRInfo',views.updateHRInfo,name='updateHRInfo')
]