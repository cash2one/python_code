#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''管道（pipeline）是redis在提供单个请求中缓冲多条服务器命令的基类的子类。
它通过减少服务器-客户端之间反复的TCP数据库包，从而大大提高了执行批量命令的功能。'''
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pipeline()
print p.set('hello','world')
print p.sadd('k','v')
print p.incr('num')
print p.execute()

p.set('hello','redis').sadd('faz','baz').incr('num').execute()