# -*- coding:utf-8 -*-
# __author__="Liyuanfang"
# __DATE__="2019/6/3"
from django.urls import path
from . import views

app_name = "triageManagement"

urlpatterns = [
    path('',views.index,name='index'),
    path('dentistList/',views.dentistList,name='dentistList'),
    path('dentistList/api/getlist',views.getlist,name='getlist'),
    path('dentistList/api/addinq',views.addin,name='addinq'),
    path('dentistList/api/initq',views.initq,name='initq'),
    path('dentistList/triage/',views.triage,name='triage'),
    path('HrForMF/',views.HrForMF,name='HrForMF'),
    path('dentistList/triage/api/adjustq',views.adjustq,name='adjustq'),
    path('dentistList/triage/api/reflashq',views.reflashq,name='reflashq'),
    path('HrForMF/api/getHRInfo',views.getHRInfo,name='getHRInfo'),
    path('HrForMF/api/updateHRInfo',views.updateHRInfo,name='updateHRInfo')
]