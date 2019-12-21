# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/6/13"
import re

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# 首页
def index(request):
    if request.session.get('username'):
        if request.session.get('role') == "患者":
            if 'quit' in request.POST:
                return render(request, "loginManagement/logout.html")
            else:
                return render(request,"patientManagement/index.html", {"username": request.session.get('username'), "userChineseName": request.session.get('userChineseName')})

    message = "对不起，您没有患者权限，请您登录！"
    return render(request, "loginManagement/login.html", {"message_origin": message})

# 退出登录
def logout(request):
    if request.method == "POST":
        status = request.POST.get("status")
        print(status)
    return JsonResponse({"status":200})

# 预约挂号页
def register(request):
    return render(request, "patientManagement/registerManagement/register.html")

# 获取次级菜单
def getDetailedRoom(request):
    if request.method == "GET":
        room = request.GET.get("room")
        sql = "SELECT DISTINCT `科室细分名称` FROM `医生` WHERE `科室名称` = %s;"
        with connection.cursor() as cursor:
            cursor.execute(sql, (room))
            results = cursor.fetchall()
        return JsonResponse({"data": results})

# 获取可挂号医生
def getDoctor(request):
    classType = {"检查号": "检查师", "普通号": "门诊医生", "专家号": "主任医师"}
    res = {"data": []}
    key = ("id", "name", "class", "no.", "location", "price", "remain")
    if request.method == "GET":
        date = request.GET.get("date")
        weekday = request.GET.get("weekday")
        detailedRoom = request.GET.get("detailedRoom")
        registerType = classType[request.GET.get("registerType")]
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "就诊记录" + year_month
        print(date, weekday, detailedRoom, registerType)
        sql = [
"DROP TABLE IF EXISTS t1;",
"""
CREATE TEMPORARY TABLE t1(
SELECT 医生.医生编号,姓名,职称,诊室名称,位置,价格,上限 
FROM 医生,挂号
WHERE 科室细分名称 = %s
AND 职称 = %s
AND 医生.医生编号 = 挂号.医生编号
AND 挂号.星期 = %s
);""",
"""SELECT * FROM t1;""",
"""
SELECT t1.医生编号,姓名,职称,诊室名称,位置,价格,(上限 - COUNT(就诊状态)) AS 剩余数量
FROM t1 LEFT JOIN """+table_name+""" 
ON 就诊日期 = DATE(%s) AND t1.医生编号 = """+table_name+""".医生编号
GROUP BY t1.医生编号,姓名,职称,诊室名称,位置,价格,上限;"""]
        print(sql)
        with connection.cursor() as cursor:
            i = 0
            results = None
            for query in sql:
                # print(query)
                if i == 0:
                    cursor.execute(query)
                    # print(0)
                elif i == 1:
                    # real_query = cursor.mogrify(query, (detailedRoom, registerType, weekday))
                    # print(real_query)
                    cursor.execute(query, (detailedRoom, registerType, weekday))
                    # print(1)
                    results = cursor.fetchall()
                elif i == 2:
                    # real_query = cursor.mogrify(query)
                    # print(real_query)
                    cursor.execute(query)
                    results = cursor.fetchall()
                else:
                    # real_query = cursor.mogrify(query, (date))
                    # print(real_query)
                    cursor.execute(query, (date))
                    results = cursor.fetchall()
                    # print(results)
                i += 1
            print(results)
            for item in results:
                print(item)
                res["data"].append(dict(zip(key, item)))
        return JsonResponse(res)

# 挂号
def registDoctor(request):
    if request.method == "POST":
        id = request.POST.get("id")
        username = request.POST.get("username")
        date = request.POST.get("date")
        weekday = request.POST.get("weekday")
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "就诊记录" + year_month
        sql = ["""
set @max_number = (select IF (MAX(挂号号码+0) IS NULL,0,MAX(挂号号码+0))
from """ + table_name + """ 
where 就诊日期 = DATE(%s));""","""
INSERT INTO """ + table_name + """ (就诊日期,挂号号码,星期,患者账号,医生编号,就诊状态) 
VALUES(DATE(%s),@max_number + 1,%s,%s,%s,'1');
"""]
        with connection.cursor() as cursor:
            # try:
            i = 0
            for query in sql:
                if i == 0:
                    real_query = cursor.mogrify(query, (date))
                    print(real_query)
                    cursor.execute(query,(date))
                    results = cursor.fetchall()
                    print(results)
                elif i == 1:
                    real_query = cursor.mogrify(query,(date,weekday,username,id))
                    print(real_query)
                    cursor.execute(query,(date,weekday,username,id))
                    results = cursor.fetchall()
                i += 1
            return JsonResponse({"status": 200})
            # except:
            #     return JsonResponse({"status":500})


