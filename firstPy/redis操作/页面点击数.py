#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set("visit:myblog:totals", 1)
#每当有一个页面点击，则使用INCR增加点击数即可。
print r.get('visit:myblog:totals')
r.incr("visit:myblog:totals")
print r.get('visit:myblog:totals')