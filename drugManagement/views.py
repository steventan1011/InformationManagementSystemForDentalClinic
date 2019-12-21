import re

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# 药品管理首页
def index(request):
    if request.session.get('username'):
        if request.session.get('role') == "取药师":
            return render(request,"drugManagement/index.html", {"username": request.session.get('username'), "userChineseName": request.session.get('userChineseName')})

    message = "对不起，您没有取药师权限，请您登录！"
    return render(request, "loginManagement/login.html", {"message_origin": message})

# 药单页
def drug(request):
    return render(request,"drugManagement/drugManagement.html")

# 个人信息页
def hr(request):
    return render(request,"drugManagement/HrForMF.html")

# api-取得药单数据
def getDrugBill(request):
    res = {"data":[]}
    key = ("id",
        "drugName",
        "specification",
        "quantity",
        "storage",
        "price")
    if request.method == "GET":
        patientID = request.GET.get("patientID")
        date = request.GET.get("date")
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "缴费单" + year_month
        sql = "SELECT 药品.药品编号,药品.药品名称,药品.药品规格, "+table_name+".单项数量,药品.库存\
            FROM  "+table_name+",药品\
            WHERE 就诊日期 = DATE(%s) AND 挂号号码 = %s AND 药品.药品编号 = "+table_name+".单项编号;"
        print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql,(date,patientID))
            results = cursor.fetchall()
        print(results)
        for item in results:
            res["data"].append(dict(zip(key,item)))
    return JsonResponse(res)

# api-更新药品和缴费单数据
def updateDrugBill(request):
    if request.method == "POST":
        value = request.POST.copy()
        patientID = value.pop("patientID")[0]
        date = value.pop("date")[0]
        newBill = map(lambda x:eval(x),value.values())
        year_month = ''.join(re.split("-", date)[:2])[2:]
        table_name = "缴费单" + year_month
        with connection.cursor() as cursor:
            for drug in newBill:
                try:
                    sql = "UPDATE "+table_name+"\
                     JOIN 药品 ON 药品.药品编号 = "+table_name+".单项编号\
                     SET 单项购买数量 = %s,库存 = %s\
                     WHERE "+table_name+".单项编号 = %s AND 药品.药品编号 = %s AND 挂号号码 = %s AND 就诊日期 = DATE(%s)"
                    cursor.execute(sql,(drug['purchaseQuantity'],drug['storage'],drug['id'],drug['id'],patientID,date))
                except:
                    return JsonResponse({"status":110})

    return JsonResponse({"status":200})

#api- 取得员工基本信息的数据
def getHRInfo(request):
    res = {"data":[]}
    key = ("id",
           "name",
           "sex",
           "dateofbirth",
           "nationality",
           "prof",
           "tele",
           "mail")
    if request.method == "GET":
        worker_id = request.GET.get("id")
        sql = "SELECT `员工编号`,`姓名`,`性别`,`生日`,`民族`,`职位`,`电话`,`邮箱`\
                FROM 医院员工\
                WHERE 员工编号 = %s"
        with connection.cursor() as cur:
            cur.execute(sql,(worker_id))
            result = cur.fetchone()
        data = dict(zip(key,result))
        data["department"] = "药房"
        res["data"].append(data)
        return JsonResponse(res)

def updateHRInfo(request):
    if request.method == "POST":
        value = request.POST.copy()
        worker_id = value.pop("id")
        with connection.cursor() as cursor:
            try:
                sql = "UPDATE `医院员工`\
                         SET `姓名` = %s,`电话` = %s,`邮箱` = %s\
                         WHERE `员工编号` = %s"

                cursor.execute(sql,(value['name'],value['tele'],value['mail'],worker_id))
            except:
                return JsonResponse({"status": 110})

    return JsonResponse({"status": 200})


