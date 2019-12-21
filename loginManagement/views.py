# login/views.py

from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from datetime import datetime

# 主页
from django.urls import reverse


def index(request):
    role = request.session.get('role')
    if role:
        if role == "医生":
            return redirect(reverse("TreatManagement:index"))
        elif role == "取药师":
            return redirect(reverse("drugManagement:index"))
        elif role == "财务":
            return redirect(reverse("finacialManagement:index"))
        elif role == "护士":
            return redirect(reverse("triageManagement:index"))
        elif role == "患者":
            return redirect(reverse("patientManagement:index"))

    return render(request, 'loginManagement/login.html')

# 登陆页
def login(request):
    # 如果点击登陆按钮
    if 'login' in request.POST:
        userPhone = request.POST.get('phone', None)
        userPassword = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if userPhone and userPassword:  # 确保用户名和密码都不为空
            userPhone = userPhone.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                sql = "SELECT  MD5(%s)"
                with connection.cursor() as cur:
                    cur.execute(sql, (userPassword))
                    userPassword = cur.fetchone()[0]

                sql = "SELECT `手机号`,`密码`, `角色`\
                                FROM 账户密码\
                                WHERE 手机号 = %s"
                with connection.cursor() as cur:
                    query = cur.mogrify(sql, (userPhone))
                    cur.execute(sql, (userPhone))
                    results = cur.fetchone()
                    password = results[1]
                    role = results[2]

                if userPassword == password:
                    request.session['role'] = role

                    if role == "医生":
                        sql = "SELECT `医生编号`, `姓名`\
                                         FROM 医生\
                                         WHERE 电话 = %s"
                        with connection.cursor() as cur:
                            cur.execute(sql, (userPhone))
                            result = cur.fetchone()
                        username = result[0]
                        userChineseName = result[1]
                        request.session['username'] = username
                        request.session['userChineseName'] = userChineseName
                        # return render(request, 'TreatManagement/IndexForDoctor.html')
                        return redirect(reverse("TreatManagement:index"))

                    elif role == "取药师":
                        sql = "SELECT `员工编号`, `姓名`\
                                         FROM 医院员工\
                                         WHERE 电话 = %s"
                        with connection.cursor() as cur:
                            query = cur.mogrify(sql, (userPhone))
                            cur.execute(sql, (userPhone))
                            result = cur.fetchone()
                        username = result[0]
                        userChineseName = result[1]
                        request.session['username'] = username
                        request.session['userChineseName'] = userChineseName
                        return redirect(reverse("drugManagement:index"))

                    elif role == "财务":
                        sql = "SELECT `员工编号`, `姓名`\
                                         FROM 医院员工\
                                         WHERE 电话 = %s"
                        with connection.cursor() as cur:
                            query = cur.mogrify(sql, (userPhone))
                            cur.execute(sql, (userPhone))
                            result = cur.fetchone()
                        username = result[0]
                        userChineseName = result[1]
                        request.session['username'] = username
                        request.session['userChineseName'] = userChineseName
                        return redirect(reverse("finacialManagement:index"))

                    elif role == "护士":
                        sql = "SELECT `员工编号`, `姓名`\
                                         FROM 医院员工\
                                         WHERE 电话 = %s"
                        with connection.cursor() as cur:
                            query = cur.mogrify(sql, (userPhone))
                            cur.execute(sql, (userPhone))
                            result = cur.fetchone()
                        username = result[0]
                        userChineseName = result[1]
                        request.session['username'] = username
                        request.session['userChineseName'] = userChineseName
                        return redirect(reverse("triageManagement:index"))

                    elif role == "患者":

                        sql = "SELECT `账号`, `姓名`\
                                         FROM 患者\
                                         WHERE 电话 = %s"
                        with connection.cursor() as cur:
                            query = cur.mogrify(sql, (userPhone))
                            cur.execute(sql, (userPhone))
                            result = cur.fetchone()
                        username = result[0]
                        userChineseName = result[1]
                        request.session['username'] = username
                        request.session['userChineseName'] = userChineseName
                        return redirect(reverse("patientManagement:index"))


                    elif role == "管理员":
                        pass

                    else:
                        pass

                else:
                    message = "密码不正确！"
            except Exception as e:
                message = "用户名不存在！"
                print(str(e))
        # return HttpResponse(json.dumps({
        #     "message": message
        # }))
        return render(request, 'loginManagement/login.html', {"message": message})

    # 如果点击注册按钮
    elif 'register' in request.POST:
        return render(request, 'loginManagement/register.html')
    return render(request, 'loginManagement/login.html')

# 注册页
def register(request):
    userphone = request.POST.get('phone')
    useremail = request.POST.get('email')
    userpassword = request.POST.get('password')
    username = request.POST.get('name')

    if request.POST.get('phone'):
        try:
            print(request.POST.get('phone'))

            sql = "SELECT `手机号`\
                                 FROM 账户密码\
                                 WHERE 手机号 = %s"
            with connection.cursor() as cur:
                query = cur.mogrify(sql, (userphone))
                cur.execute(sql, (userphone))
                result = cur.fetchone()
            if result:

                message = "该手机号已被注册，请输入其他手机号！"
                print(message)
                # return redirect(reverse("loginManagement:login"), kargs={"message": message})
                # return render(request, 'loginManagement/login.html', {"message": message})
                return render(request, 'loginManagement/register.html', {"message": message})

            else:

                sql = "insert into 账户密码(`手机号`, `密码`, `角色`) values (%s, MD5(%s), \"患者\")"
                with connection.cursor() as cur:
                    query = cur.mogrify(sql, (userphone, userpassword))
                    cur.execute(sql, (userphone, userpassword))
                sql = "SELECT COUNT(*) FROM 患者"
                with connection.cursor() as cur:
                    query = cur.mogrify(sql, ())
                    cur.execute(sql, ())
                    result = cur.fetchone()
                last = result[0]
                new = "HZ" + str(int(last)+1)
                print(new)
                print(username, useremail, userpassword, userphone)

                sql = "insert into 患者(账号, 姓名, 性别, 民族, 地址, 生日, 证件号, 证件类型, 电话, 邮箱) values (%s, %s, \"\", \"\", \"\", \"1990-01-01\", \"\", \"\", %s, %s)"
                with connection.cursor() as cur:
                    query = cur.mogrify(sql, (new, username, userphone, useremail))
                    cur.execute(sql, (new, username, userphone, useremail))
                message = "账户注册完成，开始新的旅程吧！"
                request.session['username'] = new
                request.session['userChineseName'] = username
                request.session['role'] = "患者"
                return redirect(reverse("patientManagement:index"), kargs={"message_happy": message})
                # return render(request, 'patientManagement/index.html', {"message_happy": message})
        except Exception as e:
            print(str(e))
            message = str(e)
            return render(request, 'loginManagement/register.html', {"message": message})


    return render(request, 'loginManagement/register.html')

# 登出页
def logout(request):
    # del request.session['username']
    # del request.session['userChineseName']
    # del request.session['role']
    request.session.clear()
    message = "您已登出！"
    return render(request,'loginManagement/login.html', {"message_out": message})


    # if request.method == "POST":
    #     status = request.POST.get("status")
    #     print(status)
    # return JsonResponse({"status":200})


