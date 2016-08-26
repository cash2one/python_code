import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "123", db = "querydb", charset = "utf8")

def process():
    cursor = conn.cursor()
    for line in open('/apps/home/rd/hexing/data/query_uniq'):
        word = line.strip()
        print word
        try:
            sql = """
                insert into tb_query (query) values (%s)
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(word))
            conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()
