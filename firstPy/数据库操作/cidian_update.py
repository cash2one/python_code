#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)
#conn = MySQLdb.connect(host = "127.0.0.1", user = "root", passwd = "root", db = "cidian_iciba", charset = "utf8")

def process():
    cursor = conn.cursor()
    try:
        sql = """
            select word, related_word from tb_cidian where related_word != '{}'
        """
        cursor.execute(sql)
        for (word,related_word,) in cursor.fetchall():
            res = json.loads(related_word)
            related_word_new = {}
            #print related_word
            if res.has_key(u'词汇搭配'):
                related_word_new[u'词汇搭配'] = {}
                #print res[u'词汇搭配']
                if res[u'词汇搭配'].has_key('all'):

                    #print res[u'词汇搭配']
                    related_word_new[u'词汇搭配']['all'] = []
                    _dict = {}
                    _dict['words'] = res[u'词汇搭配']['all'][0]
                    _dict['title'] = ''
                    related_word_new[u'词汇搭配']['all'].append(_dict)
                    res[u'词汇搭配'] = related_word_new[u'词汇搭配']
                    final_res = json.dumps(res)
                    print word
                    try:
                        sql = """
                            update tb_cidian set related_word=%s  where word = %s
                        """
                        # print (url, word, type, pronunciation, character, other_meaning, change, level)
                        cursor.execute(sql, (final_res, word))
                        conn.commit()
                    except:
                        traceback.print_exc()
    except:
        traceback.print_exc()

if __name__ == '__main__':
    process()