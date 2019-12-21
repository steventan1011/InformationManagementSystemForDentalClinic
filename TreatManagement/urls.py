# -*- coding:utf-8 -*-
# __author__="Liyuanfang"
# __DATE__="2019/6/10"
from django.urls import path
from . import views

app_name = "TreatManagement"


urlpatterns = [
    path('',views.index,name='index'),
    path('patientInfo/',views.patientInfo,name='patientInfo'),
    path('patientInfo/add',views.add,name='add'),
    path('patientInfo/api/updaterecord',views.updaterecord,name='updaterecord'),
    path('patientInfo/api/getdrugname',views.getdrug,name='getdrugname'),
    path('patientInfo/api/getcheckname',views.getcheck,name='getdrugname'),
    path('patientInfo/api/gettreatname',views.gettreatitem,name='getdrugname'),
    path('patientInfo/api/gettreat',views.gettreat,name='gettreat'),
    path('patientInfo/api/getpinfo',views.getpinfo,name='getpinfo'),
    path('mainInfo/',views.mainInfo,name='mainInfo'),
    path('mainInfo/api/getQueue',views.getQueue,name='getQueue'),
    path('mainInfo/api/addpatient',views.addpatient,name='addpatient'),
    path('mainInfo/api/finish',views.finish,name='finish')
]