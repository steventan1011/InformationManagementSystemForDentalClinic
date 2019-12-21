# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/6/13"
import re

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# 已挂号页面
def registedNumber(request):
    return render(request, "patientManagement/registerManagement/registedNumber.html")

# 获取今天及之后所有的已预约信息
def getRegistedNumber(request):
    res = {"data": []}
    key = ("date", "no.","name", "class", "room_no.", "location", "detailedRoom","status")
    if request.method == "GET":
        now = request.GET.get("now")
        username = request.GET.get("username")
        last = request.GET.get("last")
        now_year_month = ''.join(re.split("-", now)[:2])[2:]
        last_year_month = ''.join(re.split("-", last)[:2])[2:]
        # 月份相同
        if now_year_month == last_year_month:
            table_name = "就诊记录" + now_year_month
            sql = """SELECT 就诊日期,挂号号码,姓名,职称,诊室名称,位置,科室细分名称,就诊状态
FROM """ + table_name + """,医生
WHERE 就诊日期 >= DATE(%s) AND 就诊日期 <= DATE(%s) AND 患者账号 = %s AND """+ table_name + """.医生编号 = 医生.医生编号;"""
            with connection.cursor() as cursor:
                # real_query = cursor.mogrify(sql, (now_year_month,last_year_month,username))
                # print(real_query)
                cursor.execute(sql, (now,last,username))
                results = cursor.fetchall()
                # print(results)
                for item in results:
                    print(item)
                    res["data"].append(dict(zip(key, item)))
        # 月份不同
        else:
            table_name = "就诊记录" + now_year_month
            sql = ["""SELECT 就诊日期,挂号号码,姓名,职称,诊室名称,位置,科室细分名称,就诊状态
            FROM """ + table_name + """,医生
            WHERE 就诊日期 >= DATE(%s) AND 患者账号 = %s AND """ + table_name + """.医生编号 = 医生.医生编号;"""]
            table_name = "就诊记录" + last_year_month
            sql.append("""SELECT 就诊日期,挂号号码,姓名,职称,诊室名称,位置,科室细分名称,就诊状态
            FROM """ + table_name + """,医生
            WHERE 就诊日期 <= DATE(%s) AND 患者账号 = %s AND """ + table_name + """.医生编号 = 医生.医生编号;""")
            with connection.cursor() as cursor:
                i = 0
                results = None
                for query in sql:
                    if i == 0:
                        real_query = cursor.mogrify(query, (now, username))
                        print(real_query)
                        cursor.execute(query, (now, username))
                        results = cursor.fetchall()
                        # print(results)
                    elif i == 1:
                        real_query = cursor.mogrify(query, (last, username))
                        print(real_query)
                        cursor.execute(query, (last, username))
                        results = cursor.fetchall()
                        # print(results)
                    i += 1
                    for item in results:
                        print(item)
                        res["data"].append(dict(zip(key, item)))
                print(res)
    return JsonResponse(res)

# 患者自主退号
def rejectNumber(request):
    if request.method == "POST":
        username = request.POST.get("username")
        date = request.POST.get("date")
        regist_number = request.POST.get("no.")
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "就诊记录" + year_month
        sql = ["""SELECT 就诊状态
                    FROM """ + table_name + """
                    WHERE 就诊日期 = DATE(%s) AND 挂号号码 = %s""",
               """
               DELETE FROM """ + table_name + """
            WHERE 就诊日期 = DATE(%s) AND 挂号号码 = %s AND 就诊状态 = '1';
               """]
        with connection.cursor() as cursor:
            i = 0
            for query in sql:
                if i == 0:
                    real_query = cursor.mogrify(query, (date, regist_number))
                    print(real_query)
                    cursor.execute(query, (date, regist_number))
                    status = cursor.fetchone()
                    if status[0] != '1':
                        return JsonResponse({"status":500})
                elif i == 1:
                    real_query = cursor.mogrify(query, (date, regist_number))
                    print(real_query)
                    cursor.execute(query, (date, regist_number))
                i += 1
        return JsonResponse({"status":200})