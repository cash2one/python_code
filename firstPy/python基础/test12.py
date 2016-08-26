#-*- coding: utf-8 -*-
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","root","root","testdb" )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
#sql = "SELECT * FROM EMPLOYEE "
       #WHERE INCOME ='%d'" % (1)
sql = "insert into employee values(4)"
try:
   # 执行SQL语句
   cursor.execute(sql)
   db.commit()
   # 获取所有记录列表
   #results = cursor.fetchall()
   #print results
except:
    db.rollback()
    print "Error: unable to fecth data"

# 关闭数据库连接
db.close()