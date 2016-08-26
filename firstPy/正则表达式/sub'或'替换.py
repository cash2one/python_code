#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = 'ab cd ef gh'
print re.sub(r'ab|ef','zz',ss)