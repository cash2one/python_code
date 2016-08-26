#ecoding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def quanpai(one_res, list, res):
    if len(list) == 2:
        res.append(one_res)
    else:
        for list_str in list:
            #浅拷贝
            temp_list = list[:]
            temp_list.remove(list_str)
            quanpai(one_res + ' '+str(list_str), temp_list, res)

one_res = ''
res = []
quanpai(one_res, [1,2,3,4], res)
print res
print len(res)
