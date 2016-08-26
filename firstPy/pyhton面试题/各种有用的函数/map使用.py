#ecoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
mapper_dict = {'1': '一',
              '0': '零',
              '2': '二',
              '3': '三',
              '4': '四',
              '5': '五',
              '6': '六',
              '7': '七',
              '8': '八',
              '9': '九',
              # '10':'十'
              }


def mapper_fun(val):
    if val.isdigit() and val in mapper_dict:
        return mapper_dict[val]
    return val

name = u'深圳南山外国123语学校科苑小学'
print ''.join(map(mapper_fun, name.replace(u'深圳市', '').replace(u'深圳', '').replace(u'小学', '').replace(u'学校', '').replace(u'校区', '')))