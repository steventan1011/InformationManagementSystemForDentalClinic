# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/6/10"
from django.urls import path

from .views import register,registedNumber,userManage,treatment

app_name = "patientManagement"

urlpatterns = [
    # 预约挂号部分
    path('',register.index,name='index'),
    path('api/logout',register.logout,name='logout'),
    path('register/',register.register,name='register'),
    path('register/api/getDoctor',register.getDoctor,name='getDoctor'),
    path('register/api/getDetailedRoom',register.getDetailedRoom,name='getDetailedRoom'),
    path('register/api/registDoctor', register.registDoctor, name='registDoctor'),

    # 已挂号码部分
    path('registedNumber/',registedNumber.registedNumber,name="registerDoctor"),
    path('registedNumber/api/getRegistedNumber',registedNumber.getRegistedNumber,name="getRegistedNumber"),
    path('registedNumber/api/rejectNumber',registedNumber.rejectNumber,name="rejectNumber"),

    # 当前就诊部分
    path('treatment/',treatment.treat,name='treat'),
    path('treatment/api/getToday',treatment.getToday,name="getToday"),

    # 记录查询部分
    path('userManage/', userManage.userManage, name='userManage'),  # 个人信息管理
    path('userManage/change', userManage.userManageChange, name='userManageChange'),  # 个人信息管理
    path('userRecord/', userManage.userRecord, name='userRecord'),  # 就诊记录查询
    path('userRecord/api/getTherapy', userManage.getTherapy, name='getTherapy'),
    path('userRecord/api/getDetailBill', userManage.getDetailBill, name='getDetailBill'),
    path('userRecord/api/getDetailCheck', userManage.getDetailCheck, name='getDetailCheck'),
    path('userRecord/api/getDetailTreat', userManage.getDetailTreat, name='getDetailTreat'),
    path('userManage/api/getUser', userManage.getUser, name='getUser'),
    path('userManage/api/updateUser', userManage.updateUser, name='updateUser')
]