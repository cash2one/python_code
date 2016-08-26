#-*- coding: UTF-8 -*-
import re
text = 'a a 21  1AD<:d<d;s'
#compile相当于提取出所有满足规定正则表达式的值
pattern = re.compile('[^0-9a-zA-Z]')
result = pattern.findall(text)
print result
#re.match与re.search的区别：re.match只匹配字符串的开始，
# 如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。
if re.match('a a1',text) != None:
    print (re.match('a a1',text)).group()
print (re.search('[0-9]{2}',text)).group()
print re.sub('\s','-',text)
print re.split('\s',text)