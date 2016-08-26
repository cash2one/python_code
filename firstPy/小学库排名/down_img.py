#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys,json,oss2,hashlib,traceback,os,MySQLdb,urllib2
reload(sys)
sys.setdefaultencoding('utf-8')
conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)
cursor = conn.cursor()
cursor.execute("select id, display_image from primary_school_info")
for (id, display_image) in cursor.fetchall():
    if 'zhanqun' not in display_image:
        url = display_image
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        response = urllib2.urlopen(request)
        resp =  response.read()
        with open('/Users/bjhl/Downloads/zs.jpg','wb') as f:
            f.write(resp)
            f.flush()