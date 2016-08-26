#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)

def process():
    cursor = conn.cursor()
    for line in open('/Users/bjhl/Documents/cidian/cidian_iciba.log'):
        _dict = json.loads(line.replace('\\\\','\\'))
        word = _dict['word'].strip()
        type = []
        for each in _dict['type'].strip().split('/'):
            if each.strip() != '':
                type.append(each.strip())
        change = {}
        i = 0
        old_temp = ''
        _list = []
        for temp in _dict['change'].strip().split(u'：'):
            for each in temp.split():
                _list.append(each)
        for temp in _list:
            if i%2 == 0:
                old_temp = temp.strip()
                change[temp.strip()] = ''
            else:
                change[old_temp] = temp.strip()
            i += 1
        #print change, type
        change = json.dumps(change)
        type = json.dumps(type)
        print word
        try:
            sql = """
                update tb_cidian set ci_type=%s,ci_change=%s where word=%s
            """
            #print (url, word, type, pronunciation, character, other_meaning, change, level)
            cursor.execute(sql,(type, change, word))
            conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()