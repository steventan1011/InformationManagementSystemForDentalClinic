from django.shortcuts import render
from triageManagement.queues import Queues
from datetime import datetime
from django.db import connection
from django.http import JsonResponse
from .getDate import getDate

# Create your views here.
#主页
def index(request):
    if request.session.get('username'):
        if request.session.get('role') == "医生":
            return render(request,"TreatManagement/IndexForDoctor.html", {"username": request.session.get('username'), "userChineseName": request.session.get('userChineseName')})

    message = "对不起，您没有取药师权限，请您登录！"
    return render(request, "loginManagement/login.html", {"message_origin": message})


#患者信息页
def patientInfo(request):
    return render(request,'TreatManagement/Patient.html')

#添加就诊记录页
def add(request):
    return render(request,'TreatManagement/add(1).html')

#总信息页
def mainInfo(request):
    return render(request,'TreatManagement/main.html')

#更新在诊患者情况
def getQueue(request):
    res = {"data": []}
    key = ("name","state","id")
    date = str(datetime.now().date())
    biao = date[2:4] + date[5:7]
    if request.method == 'GET':
        doctor = request.GET.get("doctor")
        sql = "SELECT `患者`.`姓名`,`就诊状态`,挂号号码\
               FROM 就诊记录"+biao+",患者\
               WHERE 就诊日期 = date(%s) AND 医生编号 = %s AND 患者.账号=就诊记录"+biao+".患者账号 AND (就诊状态='3' or 就诊状态='4')"
        with connection.cursor() as cur:
            cur.execute(sql,(date,doctor))
            result = cur.fetchall()
        #将数据库中的数据写入res中，返回前台
        for item in result:
            res["data"].append(dict(zip(key,item)))
        return JsonResponse(res)

#新增患者进入就诊
def addpatient(request):
    res = {"data": {}}
    date = str(datetime.now().date())
    time = datetime.now()
    biao = date[2:4]+date[5:7]
    if request.method == 'GET':
        doctor = request.GET.get("doctor")
        #取得医生当前状态
        with connection.cursor() as cur:
            sql= "SELECT `当前状态`\
                   FROM 医生\
                   WHERE 医生编号 = %s"
            cur.execute(sql,(doctor))
            doctor_state = cur.fetchone()[0]
        # 判断医生是否空闲
        if doctor_state == '1':
            return JsonResponse({"status":110})
        else:
            # 获取分诊台队列数据
            q = Queues
            # 取出队首的就诊记录
            tmp = q.getpatient(q, doctor)
            #判断队列是否有元素
            if tmp == 0:
                return JsonResponse({"status": 110})
            else:
                # 修改队首的就诊记录的就诊状态，由于是从排队队列中直接取出，故不必判断是否符合状态转移条件
                with connection.cursor() as cur:
                    try:
                        # 修改就诊记录里的就诊状态
                        sql1 = "UPDATE 就诊记录"+biao+"\
                                            SET `就诊状态` = 4\
                                            WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
                        cur.execute(sql1, (date, tmp["id"]))
                        # 修改医生的状态
                        sql2 = "UPDATE `医生`\
                                            SET `当前状态` = 1\
                                            WHERE 医生编号 = %s"
                        cur.execute(sql2, (doctor))
                    except:
                        return JsonResponse({"status": 110})
                return JsonResponse({"status": 200})

#结束某一患者治疗
def finish(request):
    date = str(datetime.now().date())
    biao = date[2:4] + date[5:7]
    if request.method == 'POST':
        patientid = request.POST.get("patientid")
        doctor = request.POST.get("doctor")
        with connection.cursor() as cur:
            try:
                #修改就诊状态
                sql="UPDATE 就诊记录"+biao+"\
                     SET `就诊状态` = 6\
                     WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
                #修改医生的状态
                sql2 = "UPDATE `医生`\
                        SET `当前状态` = 0\
                        WHERE 医生编号 = %s"
                cur.execute(sql,(date,patientid))
                cur.execute(sql2,(doctor))
            except:
                return JsonResponse({"status":110})
    return JsonResponse({"status":200})

#查看患者的详细就诊记录
def gettreat(request):
    res = {"code": 0,
           "msg": "",
           "count": 1,
           "data":[]}
    key = ("date","no.","room","doctor","brief_dia","brief_res","later")
    date = str(datetime.now().date())
    biao = date[2:4] + date[5:7]
    if request.method == 'GET':
        patientid = request.GET.get("id")
        sql = "SELECT `患者账号`\
               FROM 就诊记录" + biao + "\
               WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
        with connection.cursor() as cur:
            cur.execute(sql,(date,patientid))
            huan_id = cur.fetchone()[0]
        sufs = getDate(date)
        for suf in sufs:
            sql1 = "SELECT 就诊日期,挂号号码,科室细分名称,姓名,检查结果,诊断意见,复查建议\
                    FROM 医生,就诊记录" + suf+ "\
                    WHERE 患者账号 = %s AND 医生.医生编号 = 就诊记录" + suf + ".医生编号"
            with connection.cursor() as cur:
                cur.execute(sql1,(huan_id))
                tmp = cur.fetchall()

            for item in tmp:
                res["data"].append(dict(zip(key,item)))

        return JsonResponse(res)

#查看患者的基本信息
def getpinfo(request):
    res = {"data":[]}
    key = ["患者编号","姓名","性别","年龄"]
    date = str(datetime.now().date())
    biao = date[2:4] + date[5:7]
    year = int(date[0:4])
    if request.method == 'GET':
        patientid = request.GET.get("id")
        sql = "SELECT `患者账号`\
                   FROM 就诊记录" + biao + "\
                   WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
        with connection.cursor() as cur:
            cur.execute(sql, (date, patientid))
            huan_id = cur.fetchone()[0]
        sql1 = "SELECT `账号`,姓名,性别,生日\
                   FROM 患者\
                   WHERE 账号 = %s"
        with connection.cursor() as cur:
            cur.execute(sql1, (huan_id))
            re = cur.fetchone()
        re = list(re)
        re[3] = str(year - int(str(re[3])[0:4]))
        for i in range(0,re.__len__()):
            res["data"].append({"key":key[i],"value":re[i]})
        return JsonResponse(res)

def getdrug(request):
    if request.method == 'GET':
        sql = "SELECT DISTINCT `药品名称` FROM `药品`;"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return JsonResponse({"data": results})

def getcheck(request):
    if request.method == 'GET':
        sql = "SELECT DISTINCT `检查项名称` FROM `检查项`;"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return JsonResponse({"data": results})

def gettreatitem(request):
    if request.method == 'GET':
        sql = "SELECT DISTINCT `治疗项名称` FROM `治疗项`;"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return JsonResponse({"data": results})

#更新就诊记录
def updaterecord(request):
    date = str(datetime.now().date())
    biao = date[2:4] + date[5:7]
    if request.method == 'POST':
        values = request.POST.copy()
        patientid = values.pop("patientid")
        drugs = eval(values.get("drug"))
        checks = eval(values.get("checkitem"))
        treats = eval(values.get("treatitem"))
        print(treats)
        print(values)

        with connection.cursor() as cur:
            # 更新检查相关的信息

            for check in checks:
                checkname = check["name"]
                checkres = check["inner"]
                print(patientid)
                print(checkname)
                sql0 = '''SELECT 检查结果
                                        FROM 就诊记录''' + biao + '''
                                        WHERE 就诊日期 = date(%s) AND 挂号号码 = %s'''
                print(cur.mogrify(sql0, (date, patientid)))
                cur.execute(sql0, (date, patientid))
                flag = cur.fetchone()[0]
                if flag == '':
                    sql = "UPDATE 就诊记录" + biao + "\
                                        SET `检查结果` =%s\
                                        WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
                else:
                    sql = "UPDATE 就诊记录" + biao + "\
                                        SET `检查结果` =CONCAT(检查结果,%s)\
                                        WHERE 就诊日期 = date(%s) AND 挂号号码 = %s"
                cur.execute(sql, (checkname + ":" + checkres + ";", date, patientid))

                print(checkname + ":" + checkres + ";")
                sql1 = "SELECT `检查项编号`,`价格`\
                                        FROM `检查项`\
                                        WHERE `检查项名称` like %s"
                cur.execute(sql1, ("%" + checkname + "%"))
                chetmp = cur.fetchone()
                checkid = chetmp[0]
                checkprice = chetmp[1]
                sql2 = "insert into 缴费单" + biao + "(就诊日期, 挂号号码, 单项类别, 单项编号, 单项价格, 单项数量)	values(%s, %s, \"检查项\", %s, %s, \"1\");"
                cur.execute(sql2, (date, patientid, checkid, checkprice))
            # 更新治疗相关的信息
            for treat in treats:
                treatname = treat["name"]
                sql3 = "SELECT `治疗项编号`,`价格`\
                                           FROM `治疗项`\
                                          WHERE `治疗项名称` like %s"
                cur.execute(sql3, ("%" + treatname + "%"))
                treatmp = cur.fetchone()
                treatid = treatmp[0]
                print(treatname)
                print(treatid)
                treatprice = treatmp[1]
                sql4 = "insert into 缴费单" + biao + "(就诊日期, 挂号号码, 单项类别, 单项编号, 单项价格, 单项数量)	values(%s, %s, \"治疗项\", %s, %s, \"1\");"
                cur.execute(sql4, (date, patientid, treatid, treatprice))
            # 更新药品相关信息
            for drug in drugs:
                drugname = drug["name"]
                drugnum = drug["number"]
                sql5 = "SELECT `药品编号`,`价格`\
                                            FROM `药品`\
                                            WHERE `药品名称` like %s"
                cur.execute(sql5, ("%" + drugname + "%"))
                drugtmp = cur.fetchone()
                drugid = drugtmp[0]
                print(drugid)
                drugprice = drugtmp[1]
                sql6 = "insert into 缴费单" + biao + "(就诊日期, 挂号号码, 单项类别, 单项编号, 单项价格, 单项数量)	values(%s, %s, \"药品\", %s, %s, %s);"
                cur.execute(sql6, (date, patientid, drugid, drugprice, drugnum))

            # except:
            #     return JsonResponse({"status":110})

    return JsonResponse({"status":200})
















