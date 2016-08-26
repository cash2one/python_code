#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = 'ab cd  ef gh'
tail = re.match(r'.*?([^\s]+)$',ss).group(1)
print tail
#sub和search从尾部开始都能匹配到,match却为None!!!
print re.match(r'([^ ]+)$',ss)
print re.search(r'([^ ]+)$',ss).group()
print re.sub(r'([^ ]+)$',u'尾部',ss,1)

