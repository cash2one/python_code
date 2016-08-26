#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")
#直接通过找到的接口爬取
conn = MySQLdb.connect(host = "127.0.0.1", user = "zhanqun", passwd = "wdlPD40xjO5", db = "zhanqun", charset = "utf8", port = 3305)

def process():
    cursor = conn.cursor()
    try:
        sql = """
            select id, school_name from zhongxueku
        """
        cursor.execute(sql)
        for (id, school_name,) in cursor.fetchall():
            #word = 'good'
            try:
                content = urllib2.urlopen("http://baike.baidu.com/" + word,timeout=5).read()
            except:
                traceback.print_exc()
                continue
            _dict = json.loads(content)


    except:
        traceback.print_exc()
if __name__ == '__main__':
    process()