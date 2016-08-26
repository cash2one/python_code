#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = u'12霸气公犬名字大全'
ss1 = 'せ?'
if re.findall(u'[^\u4e00-\u9fa5]+',ss):
    print 'ok'
