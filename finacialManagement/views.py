from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

# Create your views here.

 #主页
def index(request):
    if request.session.get('username'):
        if request.session.get('role') == "财务":
            return render(request,"finacialManagement/index.html", {"username": request.session.get('username'), "userChineseName": request.session.get('userChineseName')})

    message = "对不起，您没有财务权限，请您登录！"
    return render(request, "loginManagement/login.html", {"message_origin": message})

#缴费信息页
def pay(request):
    return render(request,"finacialManagement/test.html")

#员工信息页
def HrForMF(request):
    return render(request,"finacialManagement/HrForMF.html")

#获取员工的个人资料信息
def getHRInfo(request):
    res = {"data": []}
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
            cur.execute(sql, (worker_id))
            result = cur.fetchone()
        data = dict(zip(key, result))
        data["department"] = "缴费处"
        res["data"].append(data)
        return JsonResponse(res)

#更新员工的资料信息
def updateHRInfo(request):
    if request.method == 'POST':
        value = request.POST.copy()
        worker_id = value.pop("id")
        with connection.cursor() as cursor:
            try:
                sql = "UPDATE `医院员工`\
                                 SET `姓名` = %s,`电话` = %s,`邮箱` = %s\
                                 WHERE `员工编号` = %s"

                cursor.execute(sql, (value['name'], value['tele'], value['mail'], worker_id))
            except:
                return JsonResponse({"status": 110})

    return JsonResponse({"status": 200})

#获取药品缴费单数据
def getdrugPayment(request):
    res = {"data":[]}
    key = (
        "id",
        "drugname",
        "specification",
        "quantity",
        "price"
    )
    if request.method == "GET":
        patientid = request.GET.get("patientID")
        date = request.GET.get("date")
        sql = "SELECT `单项编号`,`药品名称`,`药品规格`,`单项购买数量`,`单项价格`\
                    FROM 缴费单,药品\
                    WHERE 就诊日期 = date(%s) AND 挂号号码 = %s AND 缴费单.单项编号=药品.药品编号"
        with connection.cursor() as cur:
            cur.execute(sql,(date,patientid))
            result = cur.fetchall()
        for item in result:
            res["data"].append(dict(zip(key,item)))
    return JsonResponse(res)

#更新药品缴费信息
def updatedrugPayment(request):
    if request.method == 'POST':
        value = request.POST.copy()
        date = value.pop('date')
        patientid = value.pop('patientID')
        with connection.cursor() as cur:
            try:
                 sql = "UPDATE `就诊记录`\
                                  SET `就诊状态` = 8\
                                  WHERE `就诊日期` = date(%s) AND `挂号号码`=%s"

                 cur.execute(sql,(date,patientid))
            except:
                return JsonResponse({"status": 110})
    return JsonResponse({"status": 200})

#获取检查缴费单数据
def getcheckPayment(request):
    res = {"data":[]}
    key = (
        "id",
        "checkname",
        "doctor",
        "price"
    )
    if request.method == "GET":
        patientid = request.GET.get("patientID")
        date = request.GET.get("date")
        sql = "SELECT `单项编号`,`检查项名称`,`检查医生编号`,`单项价格`\
                    FROM 缴费单,检查项\
                    WHERE 就诊日期 = date(%s) AND 挂号号码 = %s AND 缴费单.单项编号=检查项.检查项编号"
        with connection.cursor() as cur:
            cur.execute(sql,(date,patientid))
            result = cur.fetchall()
        for item in result:
            res["data"].append(dict(zip(key,item)))
    return JsonResponse(res)

def updatecheckPayment(request):
    if request.method == 'POST':
        value = request.POST.copy()
        date = value.pop('date')
        patientid = value.pop('patientID')
        with connection.cursor() as cur:
            try:
                sql = "UPDATE `就诊记录`\
                                          SET `就诊状态` = 4\
                                          WHERE `就诊日期` = date(%s) AND `挂号号码`=%s"

                cur.execute(sql, (date, patientid))
            except:
                return JsonResponse({"status": 110})
    return JsonResponse({"status": 200})
