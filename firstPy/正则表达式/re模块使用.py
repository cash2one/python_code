#ecoding:utf-8
import re
#如何匹配<html><title></title></html>得到<html>
#字符串前加r,防止转义
str = r'<html><title></title></html>'
pattern = re.compile(r'<.*?>')#为何这个只匹配<html>这一个标签????因为用的懒惰模式
'''
当正则表达式中包含能接受重复的限定符时，通常的行为是（在使整个表达式能得到匹配的前提下）匹配尽可能多的字符。以这个表达式为例：a.*b，它将会匹配最长的以a开始，以b结束的字符串。如果用它来搜索aabab的话，它会匹配整个字符串aabab。这被称为贪婪匹配。

有时，我们更需要懒惰匹配，也就是匹配尽可能少的字符。前面给出的限定符都可以被转化为懒惰匹配模式，只要在它后面加上一个问号?。这样.*?就意味着匹配任意数量的重复，但是在能使整个匹配成功的前提下使用最少的重复。现在看看懒惰版的例子吧：

a.*?b匹配最短的，以a开始，以b结束的字符串。如果把它应用于aabab的话，它会匹配aab（第一到第三个字符）和ab（第四到第五个字符）
'''
#match()只检查pattern是否在开始处匹配
print pattern.match(str).group(0)
#而 search() 则是扫描整个字符串。
print pattern.search(str).group(0)

#pattern1 = re.compile(ur'[一二三四五六七八九十、]{2}.*')
pattern1 = re.compile(ur'[一二三四五六七八九十][、].*')
str1 = u"一、了解学生心理，认识学生。"
if pattern1.match(str1):
    print True
else:
    print False

pattern2 = re.compile(ur'[0123456789]{1,2}[、].*')
str2 = u"11、了解学生心理，认识学生。"
if pattern2.match(str2):
    print True
else:
    print False

print 'asdasd'[-1]