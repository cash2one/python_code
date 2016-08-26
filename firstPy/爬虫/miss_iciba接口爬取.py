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
            select word, paraphrase, example, annotation from tb_cidian
        """
        cursor.execute(sql)
        for (word, paraphrase, example, annotation,) in cursor.fetchall():
            #word = 'good'
            try:
                content = urllib2.urlopen("http://www.iciba.com/index.php?a=getWordMean&c=search&word=" + word,timeout=5).read()
            except:
                traceback.print_exc()
                continue
            _dict = json.loads(content)

            #释义
            paraphrase = json.loads(paraphrase)
            if _dict.has_key('netmean'):
                paraphrase[u'网络释义'] = []
                if _dict['netmean'].has_key('PerfectNetExp'):
                    for each in _dict['netmean']['PerfectNetExp']:
                        _dict1 = {}
                        _dict1['name'] = each['exp']
                        _dict1['english_name'] = ''
                        _dict1['meanings'] = [each['abs']]
                        paraphrase[u'网络释义'].append(_dict1)
            if _dict.has_key('trade_means'):
                paraphrase[u'行业释义'] = _dict['trade_means']
            paraphrase = json.dumps(paraphrase)
            #print paraphrase
            #break
            #例句
            example = json.loads(example)
            if _dict.has_key('sentence'):
                example[u'双语例句'] = []
                for each in _dict['sentence']:
                    _dict1 = {}
                    _dict1['chinese'] = each['Network_cn']
                    _dict1['english'] = each['Network_en']
                    example[u'双语例句'].append(_dict1)
            example = json.dumps(example)
            #print example
            #详解
            annotation = json.loads(annotation)
            if _dict.has_key('phrase'):
                annotation[u'词组搭配'] = _dict['phrase']
            if _dict.has_key('encyclopedia'):
                annotation[u'百科'] = _dict['encyclopedia']['content']
            annotation = json.dumps(annotation)
            #print annotation
            #break
            #相关词汇
            related_word = {}
            #推荐
            recommend = {}
            ci_type = [],
            ci_character = {},
            ci_change = {},
            ci_level = 0,
            pronunciation = {},
            other_meaning = {},
            #print ci_dict
            #print zhenti
            print word
            try:
                sql = """
                    update tb_cidian set paraphrase=%s, example=%s, annotation=%s  where word = %s
                """
                #print (url, word, type, pronunciation, character, other_meaning, change, level)
                cursor.execute(sql,(paraphrase, example, annotation, word))
                conn.commit()
            except:
                traceback.print_exc()
                continue
    except:
        traceback.print_exc()
if __name__ == '__main__':
    process()