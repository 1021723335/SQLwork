import pymysql

def open():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "Yzf123456", "sushe")
    return db

def checkX(SID,Lno,Sno,MID,new):
    #检查学生正确性
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql1 = "select MID from M_table where MID = {}".format(MID)
    sql2 = "select SID from X_table where SID = {}".format(SID)
    sql3 = "select C_n from S_table where Lno = {} and Sno = {}".format(Lno,Sno)
    cursor.execute(sql1)
    results1 = cursor.fetchall()
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    cursor.execute(sql3)
    results3 = cursor.fetchall()
    if results1 == ():
        msg += '没有该宿管、'
        flag =False
    if results3 == ():
        msg += "没有该宿舍、"
        flag = False
    if results3 != () and results3[0] ==0:
        msg += "该宿舍已满、"
        flag = False
    if results2 != () and new:
        msg += "学号重复、"
        flag = False
    db.close()
    return (flag,msg)

def student_add(student):
    #增加学生
    db = open()
    cursor = db.cursor()
    sql1 = """insert into x_table(SID,Sname,Ssex,Lno,Sno,MID,Mname)
                values ("{}","{}",{},"{}","{}","{}","{}")""".format(student.SID,student.Sname,student.Ssex,student.Lno,student.Sno,student.MID,student.Mname)
    sql2 ="update s_table set C_n = C_n-1,L_n = L_n+1 where Lno = {} and Sno = {}".format(student.Lno,student.Sno)

    try:
        # 执行SQL语句
        cursor.execute(sql1)
        cursor.execute(sql2)
    except Exception as e:
        db.rollback()  # 事务回滚
        print('增加学生失败', e)
    else:
        db.commit()  # 事务提交
        print('增加学生成功', cursor.rowcount)

    # 关闭数据库连接
    db.close()

def student_delete(student):
    db = open()
    cursor = db.cursor()
    sql1 = "delete from x_table where SID = {}".format(student.SID)
    sql2 ="update s_table set C_n = C_n+1,L_n = L_n-1 where Lno = {} and Sno = {}".format(student.Lno,student.Sno)
    try:
        # 执行SQL语句
        cursor.execute(sql1)
        cursor.execute(sql2)
    except Exception as e:
        db.rollback()  # 事务回滚
        print('删除学生失败', e)
    else:
        db.commit()  # 事务提交
        print('删除学生成功', cursor.rowcount)

    # 关闭数据库连接
    db.close()

def studentLoad(table):
    #加载table表的全部信息
    db = open()
    cursor = db.cursor()
    sql = "select * from {}".format(table)

    # 执行SQL语句
    cursor.execute(sql)
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return results

def checkM(MID,new):
    #检查宿管正确性
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql = "select MID from M_table where M = {}".format(MID)
    cursor.execute(sql)
    results1 = cursor.fetchall()
    if results1 != () and new:
        msg += '已有该宿管'
        flag =False
    db.close()
    return (flag,msg)


