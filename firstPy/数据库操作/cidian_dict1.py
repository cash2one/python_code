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
            select word from tb_cidian where flag=0
        """
        cursor.execute(sql)
        for (word,) in cursor.fetchall():
            #word = 'proteolytic processin'
            try:
                content = urllib2.urlopen("http://www.iciba.com/index.php?a=getWordMean&c=search&word=" + word,timeout=5).read()
            except:
                traceback.print_exc()
                continue
            _dict = json.loads(content)
            ci_dict = {}
            if _dict.has_key('collins'):
                ci_dict[u'柯林斯高阶英汉双解学习词典'] =  _dict['collins'][0]['entry']
            if _dict.has_key('ee_mean'):
                ci_dict[u'英英词典'] = _dict['ee_mean']
            if _dict.has_key('bidec'):
                ci_dict[u'英汉双向大词典'] = _dict['bidec']['parts']
            ci_dict = json.dumps(ci_dict)
            print word
            #print ci_dict
            try:
                sql = """
                    update tb_cidian set dict=%s, flag=1  where word = %s
                """
                #print (url, word, type, pronunciation, character, other_meaning, change, level)
                cursor.execute(sql,(ci_dict, word))
                conn.commit()
            except:
                traceback.print_exc()
                continue
    except:
        traceback.print_exc()

if __name__ == '__main__':
    process()