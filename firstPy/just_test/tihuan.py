import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
dir = '/apps3/rd/yangxiaoyun/zhanqun/online/spider_data/'
filename = sys.argv[1]
fw = open(dir + filename + '.res', 'a')
with open(dir + filename) as f:
    for line in f:
        res = line.replace('analysis', 'analyse')
        fw.write(res)
        fw.flush()
fw.close()