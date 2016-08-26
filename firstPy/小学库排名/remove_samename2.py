#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import six
from six import iteritems
from six import itervalues
import mysql.connector
conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)
cursor = conn.cursor()
def test(city):
    _list = []
    cursor.execute("select id, name, district, score from primary_school_info where city='%s' and status=0;" % city)

    for (id, name, district, score) in cursor.fetchall():
        name = name.replace(u'%s' % city, '').replace('市', '').replace(district, '').replace(u"中心小学", u"小学")
        _list.append((id, name))
        #print id, name, district
    for i in range(len(_list)):
        for j in range(i + 1, (len(_list))):
            if _list[i][1] == _list[j][1]:
                print _list[i][0], _list[i][1], _list[j][0], _list[j][1]
                delete_id = max(_list[i][0], _list[j][0])
                print delete_id
                sql = "update primary_school_info set status=1 where id=%d" % delete_id
                cursor.execute(sql)
                conn.commit()

city_list = [
    u'北京',
    u'上海',
    u'广州',
    u'深圳',
    u'天津',
    u'沈阳',
    u'长春',
    u'哈尔滨',
    u'南京',
    u'杭州',
    # u'合肥',
    # u'福州',
    # u'南昌',
    # u'济南',
    # u'郑州',
    # u'武汉',
    # u'长沙',
    # u'南宁',
    # u'海口',
    # u'重庆',
    # u'成都',
    # u'贵阳',
    # u'昆明',
    # u'西安',
    # u'兰州',
    # u'西宁',
    # u'银川',
    # u'乌鲁木齐',
]
for city in city_list:
    #test(city)
    cursor.execute('''select concat('http://www.genshuixue.com/i-youshengxiao/school/', id), name,city from primary_school_info where city='%s' and status=0 order by score  limit 20''' % city)
    for (url,name,city) in cursor.fetchall():
        print url+'\t'+name+'\t'+city
