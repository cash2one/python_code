#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback,urllib2,urllib
reload(sys)
sys.setdefaultencoding("utf-8")
import socket
socket.setdefaulttimeout(3)
url ='http://bbs.csdn.net/forums/Android/closed'
url2 ='http://bbs.csdn.net/topics/391929092'
fw = open('/Users/bjhl/Documents/once_ip','a')
while True:
    ip = urllib.urlopen('http://qsrdk.daili666api.com/ip/?tid=555666178987464&num=1&delay=1&category=2').read()
    #ip = '125.39.68.70:83'
    print ip
    #break
    try:
        proxy_handler = urllib2.ProxyHandler({"http": "http://"+ip})
        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
        # 此句设置urllib2的全局opener
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        response = urllib2.urlopen(request)
        content = response.read()
        #content = urllib2.urlopen(url).read()
        print "proxy len:", len(content)
    except:
        print 'error!!!'
        continue
    try:
        proxy_handler = urllib2.ProxyHandler({"http": "http://" + ip})
        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
        # 此句设置urllib2的全局opener
        urllib2.install_opener(opener)
        request = urllib2.Request(url2)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        response = urllib2.urlopen(request)
        content = response.read()
        # content = urllib2.urlopen(url).read()
        print "proxy len:", len(content)

    except:
        print 'error!!!'
        continue
    #traceback.print_exc()
    fw.write(ip + '\n')
    fw.flush()


