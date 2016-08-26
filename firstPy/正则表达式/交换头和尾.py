#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = 'ab cd  ef gh'
head = re.match(r'[^\s]+',ss).group()
tail = re.match(r'.*?([^\s]+)$',ss).group(1)
print head,tail
ss = ss.replace(head+' ',tail+' ')
ss = ss.replace(' '+tail,' '+head)
print ss


print ss[::-1]