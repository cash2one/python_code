#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = u'2015霸气公犬名字大全'
ss1 = u'せ?'
if re.match(u'[^\u4e00-\u9fa5]+',ss):
    rep = re.match(u'[^\u4e00-\u9fa5]+',ss).group()
    ss = ss.replace(rep,'')
if ss:
    print ss
