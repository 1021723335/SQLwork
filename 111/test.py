import pymysql
# 打开数据库连接
db = pymysql.connect("localhost", "root", "Yzf123456", "sushe")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = """insert into x_table(SID,Sname,Ssex,Lno,Sno,MID,Mname)  
                values ("02180233","杨志峰","1","32","502","1","张大爷")"""
print (sql)

# 执行SQL语句
#cursor.execute(sql)
#db.commit()
# 获取所有记录列表
results = cursor.fetchall()
print(results)