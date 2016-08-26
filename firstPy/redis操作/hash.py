#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import redis
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pipeline()
p.hset('users:1','name','John')
p.hset('users:1','email','John@qq.com')
p.hset('users:1','visits',0)
p.hincrby('users:1','visits',2)
p.hgetall('users:1')
p.execute()
print r.hgetall('users:1')