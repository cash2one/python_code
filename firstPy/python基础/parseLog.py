# -*- coding: UTF-8 -*-
_dic = {'a':{'genshuixue': 1} }
_dic['a']['gen'] = 2
_dic['a']['gen'] += 2
_dic['b'] = {'gen':1}
_dic['b']['gen'] += 1
_dic['b']['gen1'] = 2

print _dic
print len(_dic)
i = 0
for key, value in _dic.items():
    i += 1
print i
# print _dic['a'][1]
# if _dic['a'][0][0] == 'genshuixue':
#      _dic['a'][0][1] += 1
# print _dic['a'][1]
# print _dic
# if _dic.has_key('a'):
#     print True


