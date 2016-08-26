#ecoding:utf-8
import random,json
print 'http://img.gsxservice.com/zhanqun/jingyan%.2d.jpg'%(random.randrange(1, 20))
for i in range(1,2):
    print i

if None:
    print 'ok'

_dict = {'1':'ok'}
_dict = json.dumps(_dict)
print type(_dict)
print type(json.JSONDecoder().decode(_dict))

print 'a   b c'.split()
print '%s%s%s' % (1,1,1)

import  sys
f = open('out.log','a')
#输出重定向
sys.stdout = f
print 'ok'