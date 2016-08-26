#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import redis
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pipeline()
p.sadd('circle:game:lol','user:debugo')
p.sadd('circle:game:lol','user:leo')
p.sadd('circle:game:lol','user:Guo')
p.sadd('circle:soccer:InterMilan','user:Guo')
p.sadd('circle:soccer:InterMilan','user:Levis')
p.sadd('circle:soccer:InterMilan','user:leo')
p.execute()
print r.smembers('circle:game:lol')
#交集
print r.sinter('circle:game:lol', 'circle:soccer:InterMilan')
#并集
print r.sunion('circle:game:lol', 'circle:soccer:InterMilan')