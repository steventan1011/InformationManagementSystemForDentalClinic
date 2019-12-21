#该函数用于获取历史就诊记录表的日期后缀

def getDate(date):
    year = date[2:4]
    month = date[5:7]
    year_dif = int(year) - 19
    month_dif = int(month) - 5
    num = year_dif * 12 + month_dif
    m = 5
    y = 19
    biaos = ['1905']
    for i in range(0, num):
        if m + 1 < 10:
            m = m + 1
            biaos.append(str(y) + "0" + str(m))
        else:
            if m + 1 > 12:
                m = 1
                y = y + 1
                biaos.append(str(y) + "0" + str(m))
            else:
                m = m + 1
                biaos.append(str(y) + str(m))
    return biaos