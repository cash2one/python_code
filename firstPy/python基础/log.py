#-*- coding: utf-8 -*-
line = "1830180	46	考研"
(c, en, en2) = line.strip('\n').split('\t')
print c,en, en2
for i in range(24):
    print '/%.2d' % (i)


import os
print os.listdir('/usr/local')[0]

from collections import defaultdict
_dict = {}
if 'a' not in _dict:
    _dict['a'] = defaultdict(int)
#加了defaultdict就又一个默认值了
_dict['a']['b'] += 1
print _dict
print _dict['a']
print _dict['a']['b']
for key, value in _dict.iteritems():
    print key,value
    for k, v in value.iteritems():
        print k,v


print __file__


import  datetime
which_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
print which_day
print datetime.datetime.now().strftime('%H')

lastday =datetime.datetime.now() - datetime.timedelta(days=1)
print lastday
last2day =  (lastday - datetime.timedelta(days=1)).strftime('%Y%m%d')
print last2day

baizhan_china_dic = {'英语': 'yingyu', '语文': 'yuwen'}
for k in baizhan_china_dic:
    print k
result_dict = {k: {'home': [0, set()], 'list': [0, set()], 'detail': [0, set()], 'course': [0, set()], 'all_uv': set()} for k in baizhan_china_dic }
print result_dict

#print {v:k  for k, v in baizhan_china_dic.iteritems()}
kk = baizhan_china_dic.get('英语','语文')
print kk
d=[]
d.append({'a':1,'b':2,'c':3})
d.append({'a':11,'b':22,'c':33})
for v in d:
    print v['a']
