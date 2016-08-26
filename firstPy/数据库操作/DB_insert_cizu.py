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
    for line in open('/Users/bjhl/Documents/duanyu_youdao'):
        _dict = json.loads(line.strip().replace('\\\\','\\'))
        word = _dict['word'].strip()
        #print type
        paraphrase = json.dumps(_dict['paraphrase'])
        example = json.dumps(_dict['example'])
        annotation = json.dumps(_dict['annotation'])
        related_word = json.dumps(_dict['related_word'])
        recommend = json.dumps(_dict['recommend'])
        ci_type = json.dumps([])
        ci_change = json.dumps(_dict['ci_change'])
        #title = json.dumps(_dict['title'])
        dict = json.dumps(_dict['dict'])
        other_meaning = json.dumps(_dict['other_meaning'])
        url = json.dumps(_dict['url'])
        pronunciation = json.dumps(_dict['pronunciation'])
        question = json.dumps(_dict['question'])
        ci_character = json.dumps(_dict['ci_character'])
        ci_level = json.dumps(_dict['ci_level'])

        print '%s' % word
        try:
            sql = """
                 insert into tb_cidian (word, paraphrase,example,annotation,related_word,recommend,ci_type,ci_change,
                 dict,other_meaning,url,pronunciation,question,ci_character,ci_level) values (%s,%s, %s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(word,paraphrase,example,annotation,related_word,recommend,ci_type,ci_change,dict,other_meaning,url,pronunciation,question,ci_character,ci_level))
            conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()