#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)
#conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "root", db = "cidian_iciba", charset = "utf8")
fw = open('/Users/bjhl/Documents/cidian/close_words.txt','a')
def process():
    cursor = conn.cursor()
    try:
        sql = """
            select word, recommend from tb_cidian where recommend != '{}' and flag=1
        """
        cursor.execute(sql)
        for (word,recommend,) in cursor.fetchall():
            res = json.loads(recommend)
            #print recommend
            if res.has_key(u'临近单词'):
                for each in res[u'临近单词']:
                    fw.write(each+'\n')
                    fw.flush()
                print word
                try:
                    sql = """
                        update tb_cidian set flag=%s  where word = %s
                    """
                    # print (url, word, type, pronunciation, character, other_meaning, change, level)
                    cursor.execute(sql, (0, word))
                    conn.commit()
                except:
                    traceback.print_exc()
    except:
        traceback.print_exc()

if __name__ == '__main__':
    process()