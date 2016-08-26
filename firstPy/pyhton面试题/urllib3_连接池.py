# coding=utf8
import urllib3
import datetime
import time
import urllib

#创建连接特定主机的连接池
http_pool = urllib3.HTTPConnectionPool('ent.qq.com')
#获取开始时间
strStart = time.strftime('%X %x %Z')
for i in range(0,100,1):
    print i
    #组合URL字符串
    url = 'http://ent.qq.com/a/20111216/%06d.htm' % i
    print url
    #开始同步获取内容
    r = http_pool.urlopen('GET',url,redirect=False)
    print r.status
    print r.headers
    print r.data
#打印时间
print 'start time : ',strStart
print 'end time : ',time.strftime('%X %x %Z')