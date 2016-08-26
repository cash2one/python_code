#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = 'ab cd  ef gh'
#捕获组一定要加括号()
print re.match(r'(.*?) (.*) (.*)',ss).group()#打印全部
print re.match(r'(.*?) (.*) (.*)',ss).group(1)#第一组
print re.match(r'(.*?) (.*) (.*)',ss).group(2)#第二组
print re.match(r'(.*?) (.*) (.*)',ss).group(3)#第三组
head = re.match(r'(.*?) (.*) (.*)',ss).group(1)
tail = re.match(r'(.*?) (.*) (.*)',ss).group(3)
ss = re.sub(r'(.*?) ',tail+' ',ss,1)
print ss
#尾部替换有点特殊
ss = re.sub('([^\s]+)$',head,ss,1)
print ss

