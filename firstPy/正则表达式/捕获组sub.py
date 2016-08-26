#ecoding:utf-8
import re,sys
reload(sys)
sys.setdefaultencoding("utf-8")
ss = 'ab cd ef gh'
#捕获组的sub,比如\6，表示匹配前面pattern中的第6个group
print re.sub(r'(.*?)\s(.*)\s(.*) \1','\g<1>',ss,1)
inputStr = "hello crifan, nihao crifan";
replacedStr = re.sub(r"hello (.*?), nihao \1", "crifanli", inputStr);
print "replacedStr=",replacedStr; #crifanli

ss.en

#怎么就把中间给替换掉了呢?
print re.sub(r'(.*?)\s(.*)\s(.*) \1','zz',ss)
print re.sub(r'(.*?)\s(.*)\s(.*) \2','zz',ss)
print re.sub(r'(.*?)\s(.*)\s(.*) \3','zz',ss)
print re.match(r'(.*?)\s(.*)\s(.*)',ss).group(2)