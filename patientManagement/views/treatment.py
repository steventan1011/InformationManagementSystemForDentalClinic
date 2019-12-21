# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/6/13"
import re

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# 预约挂号页
def treat(request):
    return render(request, "patientManagement/visitManagement/now.html")

# 获得当天就诊数据
def getToday(request):
    res = {"data": []}
    key = ( "date","num","room","detroom","place","doctor","state")
    if request.method == "GET":
        date = request.GET.get("date")
        username = request.GET.get("username")
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "就诊记录" + year_month
        sql = """SELECT 就诊日期,挂号号码,科室名称,科室细分名称,位置,姓名,就诊状态
FROM """ + table_name + """,医生
WHERE 就诊日期 = DATE(%s) AND 患者账号 = %s AND """ + table_name + """.医生编号 = 医生.医生编号;"""
        with connection.cursor() as cursor:
            # real_query = cursor.mogrify(sql, (now_year_month,last_year_month,username))
            # print(real_query)
            cursor.execute(sql, (date, username))
            results = cursor.fetchall()
            # print(results)
            for item in results:
                print(item)
                res["data"].append(dict(zip(key, item)))
            print(res)
    return JsonResponse(res)
