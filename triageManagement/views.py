from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from .queues import Queues

# Create your views here.

#主页
def index(request):
    if request.session.get('username'):
        if request.session.get('role') == "护士":
            if 'quit' in request.POST:
                return render(request, "loginManagement/logout.html")
            else:
                return render(request,"triageManagement/index.html", {"username": request.session.get('username'), "userChineseName": request.session.get('userChineseName')})

    message = "对不起，您没有护士权限，请您登录！"
    return render(request, "loginManagement/login.html", {"message_origin": message})

#分诊台页面
def dentistList(request):
    return render(request,'triageManagement/dentistList.html')

#排队页面
def triage(request):
    return render(request,'triageManagement/Triage.html')

#个人信息页面
def HrForMF(request):
    return render(request,'triageManagement/HrForMF.html')

#分诊台获取各科室医生数据
def getlist(request):
    res = {"data":[]}
    key = ("id","name","pro","detroom","room")
    sections = ["牙体牙髓科",
           "牙周科",
           "整形科",
           "牙槽外科",
           "外伤肿瘤科",
           "颞下颌关节科",
           "口腔修复科",
           "口腔正畸科",
           "口腔种植科",
           "口腔黏膜科",
           "口腔儿童牙科"]
    if request.method == 'GET':
        for section in sections:
            #tmp变量保存科室对应的医生列表
            tmp = {"type":section,"list":[]}
            sql1 = "SELECT `医生编号`,姓名,职称,科室细分名称,诊室名称\
                FROM 医生\
                WHERE 科室细分名称 = %s"
            with connection.cursor() as cur:
                cur.execute(sql1,(section))
                result = cur.fetchall()
            for item in result:
                tmp["list"].append(dict(zip(key,item)))
            res["data"].append(tmp)
        return JsonResponse(res)

#分诊台排队系统信息
def addin(request):
    key=("doctor_id","id","name","doctor","section","room")
    date = str(datetime.now().date())
    biao = date[2:4]+date[5:7]
    if request.method=='GET':
        patientid=request.GET.get("patientid")
        #获取就诊状态
        sql1 = "SELECT `就诊状态`\
                FROM 就诊记录"+biao+"\
                WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
        with connection.cursor() as cur:
            cur.execute(sql1,(date,patientid))
            state = cur.fetchone()[0]
        # 当就诊记录状态符合转换条件时才允许进行加入排队队列操作
        if state == '1':
            #先对就诊记录的就诊状态进行修改，修改为排队中的状态
            with connection.cursor() as cur:
                try:
                    sql2 = "UPDATE 就诊记录"+biao+"\
                            SET `就诊状态` = 3\
                            WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
                    cur.execute(sql2,(date,patientid))
                except:
                    return JsonResponse({"status":110})
            #再对排队队列进行修改，将该就诊记录信息添加进排队队列中
            sql3 = "SELECT `医生`.`医生编号`,`挂号号码`,`患者`.`姓名`,`医生`.`姓名`,`科室细分名称`,`诊室名称`\
                    FROM 就诊记录"+biao+",患者,医生\
                    WHERE 就诊日期 = date(%s) AND 挂号号码 = %s AND 患者.账号=就诊记录"+biao+".患者账号 AND 医生.医生编号 = 就诊记录"+biao+".医生编号"
            with connection.cursor() as cur:
                cur.execute(sql3, (date, patientid))
                result = cur.fetchone()
            data = dict(zip(key, result))
            q = Queues
            q.addinq(q, data["doctor_id"], data)
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":110})

#刷新分诊台排队信息
def reflashq(request):
    res = {"data":[]}
    if request.method == 'GET':
        doctor = request.GET.get("doctor")
        q = Queues
        data = q.showq(q,doctor)
        print(data)
        if data == 0:
            return JsonResponse({"status":110})
        else:
            res["data"] = data
            return JsonResponse(res)

#获取分诊台排队系统队列调整信息
def adjustq(request):
    if request.method == 'POST':
        list = []
        data = request.POST.copy()
        print(data)
        doctor = data.pop("doctor")[0]
        print(doctor)
        maps = map(lambda x:eval(x),data.values())
        for item in maps:
            list.append(item)
        q = Queues
        a = q.adjustq(q,doctor,list)
        if a==0:
            return JsonResponse({"status":110})
        # print(q.showq(q,doctor))

    return JsonResponse({"status":200})

#分诊台排队数据初始化
def initq(request):
    date = str(datetime.now().date())
    key = ("doctor_id", "id", "name", "doctor", "section", "room")
    biao = date[2:4] + date[5:7]
    if request.method == 'GET':
        sql1 = "SELECT `医生`.`医生编号`,`挂号号码`,`患者`.`姓名`,`医生`.`姓名`,`科室细分名称`,`诊室名称`\
                    FROM 就诊记录"+biao+",患者,医生\
                    WHERE 就诊状态 = '2' AND 就诊日期 = date(%s) AND 患者.账号=就诊记录"+biao+".患者账号 AND 医生.医生编号 = 就诊记录"+biao+".医生编号"
        with connection.cursor() as cur:
            cur.execute(sql1,(date))
            result = cur.fetchall()
        for item in result:
            data = dict(zip(key, item))
            q = Queues
            q.addinq(q, data["doctor_id"], data)
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

#api-保存修改的员工信息
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
