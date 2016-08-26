#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import urllib2,urllib
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding("utf-8")

#print urllib2.urlopen('http://www.cfa.cn/cfa/').read()
print pq(urllib.urlopen('http://www.cfa.cn/cfa/').read()).html()