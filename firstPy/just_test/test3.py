#ecoding:utf-8

import os,sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")
_dict = {'a':'b'}
if _dict.has_key('id'):
    _dict.pop('id')
print _dict.get('c','')
print len(_dict)
del _dict['a']
print len(_dict)

_d = {}
for each in _d.iteritems():
    print each

se = set()
se.add('啊')
se.add('12')
se.add('啊')
se.add('123')
print ','.join(se)

ss = ('\t'.split('\t'))
print len (ss)
if '' not in ss:
    print 'ok'


import re
name = u'广州与清晰区大空间都会区看见小学'
add_part = re.match(ur'.*?区', name).group(0)
add_part = re.sub(ur'.*?市','', add_part)
print add_part


import os
print __file__
print os.path.dirname(__file__)+'/templates'
print os.path.join(os.path.dirname(__file__),'templates')

import random
print type(random.choice)


#json文件都是双引号
json_dict = '{"tag":"python"}'
print json.loads(json_dict)