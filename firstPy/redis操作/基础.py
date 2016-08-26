#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('guo','shuai')
r.set('k','v')
print r.get('guo')
print r['guo']
print r.keys()
print r.dbsize()
print r.delete('guo')
print r.save()
print r.flushdb()