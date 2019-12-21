# -*- coding:utf-8 -*-
# __author__="BaiShunqin"
# __DATE__="2019/6/13"
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def allKindReturn(s, sdate, edate, userAccount):
    resultsSet = []
    if s == 1:  # 56 all
        print(1)
        sql1 = """SELECT `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                        SUM(`缴费单1905`.`单项价格`*`缴费单1905`.`单项购买数量`) 
                        FROM 就诊记录1905,医生,缴费单1905 
                        WHERE `就诊记录1905`.`患者账号` = %s  
                        AND `就诊记录1905`.`医生编号` = `医生`.`医生编号`  
                        AND `就诊记录1905`.`就诊日期`=`缴费单1905`.`就诊日期` AND `就诊记录1905`.`挂号号码`=`缴费单1905`.`挂号号码` 
                        GROUP BY `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`"""
        with connection.cursor() as cursor:
            cursor.execute(sql1, userAccount)
            results = cursor.fetchall()
        for item in results:
            resultsSet.append(item)
        sql2 = """SELECT `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                                SUM(`缴费单1906`.`单项价格`*`缴费单1906`.`单项购买数量`) 
                                FROM 就诊记录1906,医生,缴费单1906 
                                WHERE `就诊记录1906`.`患者账号` = %s  
                                AND `就诊记录1906`.`医生编号` = `医生`.`医生编号`  
                                AND `就诊记录1906`.`就诊日期`=`缴费单1906`.`就诊日期` AND `就诊记录1906`.`挂号号码`=`缴费单1906`.`挂号号码` 
                                GROUP BY `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`"""
        with connection.cursor() as cursor1:
            cursor1.execute(sql2, userAccount)
            results1 = cursor1.fetchall()
        for item1 in results1:
            resultsSet.append(item1)
        print(resultsSet)
        return resultsSet

    if s == 2:  # 5all 6<=enddate
        print(2)
        sql1 = """SELECT `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                                SUM(`缴费单1905`.`单项价格`*`缴费单1905`.`单项购买数量`) 
                                FROM 就诊记录1905,医生,缴费单1905 
                                WHERE `就诊记录1905`.`患者账号` = %s AND `就诊记录1905`.`就诊日期` >= DATE(%s) 
                                AND `就诊记录1905`.`医生编号` = `医生`.`医生编号`  
                                AND `就诊记录1905`.`就诊日期`=`缴费单1905`.`就诊日期` AND `就诊记录1905`.`挂号号码`=`缴费单1905`.`挂号号码` 
                                GROUP BY `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`"""
        with connection.cursor() as cursor:
            cursor.execute(sql1, (userAccount, sdate))
            results = cursor.fetchall()
        for item in results:
            resultsSet.append(item)
        sql2 = """SELECT `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                                        SUM(`缴费单1906`.`单项价格`*`缴费单1906`.`单项购买数量`) 
                                        FROM 就诊记录1906,医生,缴费单1906 
                                        WHERE `就诊记录1906`.`患者账号` = %s AND `就诊记录1906`.`就诊日期` <= DATE(%s) 
                                        AND `就诊记录1906`.`医生编号` = `医生`.`医生编号`  
                                        AND `就诊记录1906`.`就诊日期`=`缴费单1906`.`就诊日期` AND `就诊记录1906`.`挂号号码`=`缴费单1906`.`挂号号码` 
                                        GROUP BY `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`"""
        with connection.cursor() as cursor1:
            cursor1.execute(sql2, (userAccount, edate))
            results1 = cursor1.fetchall()
        for item1 in results1:
            resultsSet.append(item1)
        print(resultsSet)
        return resultsSet

    if s == 3:  # 6 sdate-enddate
        print(3)
        sql2 = """SELECT `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`,
                                        SUM(`缴费单1906`.`单项价格`*`缴费单1906`.`单项购买数量`)
                                        FROM 就诊记录1906,医生,缴费单1906
                                        WHERE `就诊记录1906`.`患者账号` = %s AND `就诊记录1906`.`就诊日期` >= DATE(%s) AND `就诊记录1906`.`就诊日期` <= DATE(%s)
                                        AND `就诊记录1906`.`医生编号` = `医生`.`医生编号` 
                                        AND `就诊记录1906`.`就诊日期`=`缴费单1906`.`就诊日期` AND `就诊记录1906`.`挂号号码`=`缴费单1906`.`挂号号码`
                                        GROUP BY `就诊记录1906`.`就诊日期`,`就诊记录1906`.`挂号号码`"""
        with connection.cursor() as cursor1:
            query = cursor1.mogrify(sql2, (userAccount, sdate, edate))
            print(query)
            cursor1.execute(sql2, (userAccount, sdate, edate))
            results1 = cursor1.fetchall()
        for item1 in results1:
            resultsSet.append(item1)
        print(resultsSet)
        return resultsSet

    if s == 4:  # 5 sdate-edate
        print(4)
        sql2 = """SELECT `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`,`医生`.`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                                                        SUM(`缴费单1905`.`单项价格`*`缴费单1905`.`单项购买数量`) 
                                                        FROM 就诊记录1905,医生,缴费单1905 
                                                        WHERE `就诊记录1905`.`患者账号` = %s AND `就诊记录1905`.`就诊日期` >= DATE(%s) AND `就诊记录1905`.`就诊日期` <= DATE(%s) 
                                                        AND `就诊记录1905`.`医生编号` = `医生`.`医生编号`  
                                                        AND `就诊记录1905`.`就诊日期`=`缴费单1905`.`就诊日期` AND `就诊记录1905`.`挂号号码`=`缴费单1905`.`挂号号码` 
                                                        GROUP BY `就诊记录1905`.`就诊日期`,`就诊记录1905`.`挂号号码`"""
        with connection.cursor() as cursor1:
            cursor1.execute(sql2, (userAccount, sdate, edate))
            results1 = cursor1.fetchall()
        for item1 in results1:
            resultsSet.append(item1)
        print(resultsSet)
        return resultsSet

# 用户个人信息页


def userManage(request):
    return render(request, "patientManagement/userManagement/userManagement.html")


def userManageChange(request):
    return render(request, "patientManagement/userManagement/change.html")

# 用户就诊记录页


def userRecord(request):
    return render(request, "patientManagement/userManagement/visitingRecord.html")

# 获取就诊记录
def getTherapy(request):
    res = {"data": []}
    key = ("date",
           "no.",
           "doctor",
           "room",
           "description",
           "diagnosis",
           "result",
           "treatment",
           "later",)
    if request.method == "GET":
        results = []
        useraccount = request.GET.get("userAccount")
        startdate = request.GET.get("startdate")
        enddate = request.GET.get("enddate")
        startYear = int(request.GET.get("startYear"))
        startMonth = int(request.GET.get("startMonth"))
        endYear = int(request.GET.get("endYear"))
        endMonth = int(request.GET.get("endMonth"))
        '''sql1 = "SELECT `就诊日期`,`挂号号码`,`医生`,`姓名`,`科室名称`,`主诉`,`检查结果`,`诊断意见`,`治疗意见`,`复查建议`, 
                SUM(`缴费单`.`单项价格`*`缴费单`.`单项购买数量`) 
                FROM 就诊记录,医生,缴费单 
                WHERE 就诊日期 >= DATE(%s) AND 就诊日期 <= DATE(%s)and `患者`.`账号` = %s  
                AND `就诊记录`.`医生编号` = `医生`.`医生编号`  
                AND `就诊记录`.`就诊日期`=`缴费单`.`就诊日期` AND `就诊记录`.`挂号号码`=`缴费单`.`挂号号码` 
                GROUP BY `就诊记录`.`就诊日期`,`就诊记录`.`挂号号码`"
        with connection.cursor() as cursor:
            cursor.execute(sql1,(date1,date2,userAccount))
            results = cursor.fetchall()'''
        if startYear > 2019:
            print(1)
            return JsonResponse({"status": 110})
        else:
            if (startYear < 2019) or (startYear == 2019 and startMonth < 5):
                if endYear < 2019:
                    print(2)
                    return JsonResponse({"status": 101})
                if endYear > 2019:
                    print(3)
                    results = allKindReturn(1, startdate, enddate, useraccount)
                    for item in results:
                        res["data"].append(dict(zip(key, item)))
                    return JsonResponse(res)
                else:
                    if endMonth < 5:
                        print(4)
                        return JsonResponse({"status": 101})
                    if endMonth > 6:
                        print(5)
                        results = allKindReturn(
                            1, startdate, enddate, useraccount)
                        for item in results:
                            res["data"].append(dict(zip(key, item)))
                        return JsonResponse(res)
                    if endMonth == 5:
                        print(6)
                        results = allKindReturn(
                            4, startdate, enddate, useraccount)
                        for item in results:
                            res["data"].append(dict(zip(key, item)))
                        return JsonResponse(res)
                    if endMonth == 6:
                        print(7)
                        results = allKindReturn(
                            2, startdate, enddate, useraccount)
                        for item in results:
                            res["data"].append(dict(zip(key, item)))
                        return JsonResponse(res)

            if startYear == 2019 and startMonth > 6:
                print(8)
                return JsonResponse({"status": 110})

            else:
                if endYear > 2019:
                    print(9)
                    results = allKindReturn(1, startdate, enddate, useraccount)
                    for item in results:
                        res["data"].append(dict(zip(key, item)))
                    return JsonResponse(res)
                else:
                    if endMonth == 5:
                        print(10)
                        results = allKindReturn(
                            4, startdate, enddate, useraccount)
                        for item in results:
                            res["data"].append(dict(zip(key, item)))
                        return JsonResponse(res)
                    else:
                        if startMonth == 5:
                            print(11)
                            results = allKindReturn(
                                2, startdate, enddate, useraccount)
                            for item in results:
                                res["data"].append(dict(zip(key, item)))
                            return JsonResponse(res)
                        else:
                            print(12)
                            results = allKindReturn(
                                3, startdate, enddate, useraccount)
                            for item in results:
                                res["data"].append(dict(zip(key, item)))
                            return JsonResponse(res)

# api-查找药单


def getDetailBill(request):
    res = {"data": []}
    key = ("drugName",
           "specification",
           "quantity",
           "price")
    if request.method == "GET":
        date = request.GET.get("date")
        number = request.GET.get("no.")
        month = date.split('-')[1]
        if month == '05':
            sql = """SELECT 药品.药品名称, 药品.药品规格, 缴费单1905.单项购买数量, 药品.价格 
                FROM 缴费单1905,药品 
                WHERE 缴费单1905.就诊日期=DATE(%s) and 缴费单1905.挂号号码=%s and 缴费单1905.单项编号=药品.药品编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))
        if month == '06':
            sql = """SELECT 药品.药品名称, 药品.药品规格, 缴费单1906.单项购买数量, 药品.价格 
                FROM 缴费单1906,药品 
                WHERE 缴费单1906.就诊日期=DATE(%s) and 缴费单1906.挂号号码=%s and 缴费单1906.单项编号=药品.药品编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))

    return JsonResponse(res)

# api-查找检查单


def getDetailCheck(request):
    res = {"data": []}
    key = (
        "checkName",
        "quantity",
        "price")
    if request.method == "GET":
        date = request.GET.get("date")
        number = request.GET.get("no.")
        month = date.split('-')[1]
        if month == '05':
            sql = """SELECT 检查项.检查项名称, 缴费单1905.单项购买数量, 检查项.价格 
                FROM 缴费单1905,检查项 
                WHERE 缴费单1905.就诊日期=DATE(%s) and 缴费单1905.挂号号码=%s and 缴费单1905.单项编号=检查项.检查项编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))
        if month == '06':
            sql = """SELECT 检查项.检查项名称, 缴费单1906.单项购买数量, 检查项.价格 
                FROM 缴费单1906,检查项 
                WHERE 缴费单1906.就诊日期=DATE(%s) and 缴费单1906.挂号号码=%s and 缴费单1906.单项编号=检查项.检查项编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))
        print(res)

    return JsonResponse(res)

# api-查找治疗单


def getDetailTreat(request):
    res = {"data": []}
    key = (
        "treatName",
        "quantity",
        "price")
    if request.method == "GET":
        date = request.GET.get("date")
        number = request.GET.get("no.")
        month = date.split('-')[1]
        if month == '05':
            sql = """SELECT 治疗项.治疗项名称, 缴费单1905.单项购买数量, 治疗项.价格 
                FROM 缴费单1905,治疗项 
                WHERE 缴费单1905.就诊日期=DATE(%s) and 缴费单1905.挂号号码=%s and 缴费单1905.单项编号=治疗项.治疗项编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))
        if month == '06':
            sql = """SELECT 治疗项.治疗项名称, 缴费单1906.单项购买数量, 治疗项.价格 
                FROM 缴费单1906,治疗项 
                WHERE 缴费单1906.就诊日期=DATE(%s) and 缴费单1906.挂号号码=%s and 缴费单1906.单项编号=治疗项.治疗项编号"""
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, number))
                results = cursor.fetchall()
            for item in results:
                res["data"].append(dict(zip(key, item)))

    return JsonResponse(res)


def getUser(request):
    res = {"data": []}
    key = (
        "name",
        "sex",
        "dateofbirth",
        "nationality",
        "id_type",
        "id_number",
        "tele",
        "address"
    )
    if request.method == "GET":
        user_id = request.GET.get("id")
        sql = """SELECT `姓名`,`性别`,`生日`,`民族`,`证件类型`,`证件号`,`电话`,`地址` 
                FROM 患者 
                WHERE 账号 = %s"""
        print(user_id)
        with connection.cursor() as cur:
            cur.execute(sql, (user_id))
            result = cur.fetchone()
        print(result)
        data = dict(zip(key, result))
        res["data"].append(data)
        print(res)
        return JsonResponse(res)


def updateUser(request):
    if request.method == "POST":
        value = request.POST.copy()
        print(value)
        user_id = value.pop("userID")
        with connection.cursor() as cursor:
            try:
                sql = """UPDATE 患者 
                         SET 姓名 = %s,电话 = %s,地址 = %s,性别 = %s,生日 = date(%s),民族 = %s 
                         WHERE 账号 = %s"""
                sql1 = """UPDATE 患者 SET 姓名 = "+value['input_name']+",电话 = "+value['input_tele']+",地址 = "+value['input_address'] +  
                    "，性别 = "+value['input_sex']+"，生日 = "+value['input_dateofbirth'] +  
                    "，民族 = "+value['input_nationality']+" WHERE 账号 = %s"""
                print(sql1)

                cursor.execute(sql, (value['input_name'], value['input_tele'], value['input_address'],
                                     value['input_sex'], value['input_dateofbirth'], value['input_nationality'], user_id))
            except:
                return JsonResponse({"status": 110})

    return JsonResponse({"status": 200})
