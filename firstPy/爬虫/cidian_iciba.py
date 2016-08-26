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
    for line in open('/Users/bjhl/Documents/ciku.txt'):
        word = line.strip().replace('\n','')
        try:
            content = urllib2.urlopen("http://www.iciba.com/index.php?a=getWordMean&c=search&word=" + word,timeout=5).read()
        except:
            traceback.print_exc()
            continue
        _dict = json.loads(content)
        #词典
        collins = {}
        if _dict.has_key('collins'):
            collins = _dict['collins'][0]['entry'][0]
        #真题
        cetFour = {}
        if _dict.has_key('cetFour'):
            cetFour = _dict['cetFour']['Sentence'][0]
        cetSix = {}
        if _dict.has_key('cetSix'):
            cetSix = _dict['cetSix']['Sentence'][0]
        ci_dict = {}
        ci_dict.update(collins)
        zhenti = {}
        zhenti['cetFour'] = cetFour
        zhenti['cetSix'] = cetSix
        ci_dict = json.dumps(ci_dict)
        zhenti = json.dumps(zhenti)
        #print ci_dict
        #print zhenti
        print word
        try:
            sql = """
                update tb_cidian set dict=%s, question=%s  where word = %s and question is null
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(ci_dict, zhenti, word))
            conn.commit()
        except:
            traceback.print_exc()
            continue
if __name__ == '__main__':
    process()