#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")
dir = '/apps3/rd/yangxiaoyun/zhanqun/online/spider_data/'
filename = 'chengxuyuan_boke.res'
fw = open(dir + filename + '2', 'a')
with open(dir + filename) as f:
    for line in f:
        res = line.replace('"', '\\"').replace('${', '$"{')+'\"'
        fw.write(res)
        fw.flush()
fw.close()