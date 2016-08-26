#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123",db="resultdb", charset="utf8")
rootdir = '/apps/home/rd/zengsheng/'
filename = sys.argv[1]
cursor = conn.cursor()
_list = []
for line in open(rootdir+filename):
    taskid = line.strip().split('$$$$$')[0]
    #print taskid
    _list.append(taskid)
    if len(_list) > 100:
        taskids =  ','.join("'"+v+"'" for v in _list)
        print taskids
        _list = []
        try:
            sql = '''delete from '''+filename+''' where taskid in ('''+taskids+''')'''
            cursor.execute(sql)
            conn.commit()
        except:
            traceback.print_exc()
if len(_list) != 0:
    taskids = ','.join("'" + v + "'" for v in _list)
    print taskids
    _list = []
    try:
        sql = '''delete from ''' + filename + ''' where taskid in (''' + taskids + ''')'''
        cursor.execute(sql)
        conn.commit()
    except:
        traceback.print_exc()
