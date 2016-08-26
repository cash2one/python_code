#-*- coding: utf-8 -*-
print hex(16);
print oct(8)
print bin(2)
#将对象 x 转换为字符串
print str("123")
#将对象x转换为表达式字符串,会带引号
print repr("123")
#转成字符
print chr(65)
#转成数字
print ord('A')
import  math
print math.pi
print math.e
#想输出'\as\d'
print "\\as\d"
#三引号作用——所见即所得
print '''hi
everybody'''
print 'hi\
everybody'
#Unicode字符串,u0020是python的Unicode编码
print 'Hello\nworld'
print 'Hello\u0020world'
print u'Hello\nworld'
print u'Hello\u0020world'
#python的字符串内建函数
print "asd".capitalize()
print "asd".center(7)
print "asdasdasd".count('as',0,5)
print "asdasdasd".endswith('as',0,5)
print "asdasdasd".find('ss',2,5)
print "asd123<>?".isalnum()
print "asd123".isalnum()
print "123A".isupper()
print max("1239asdASD"),min("9asdASD")
print "asdasd asd".title()

print cmp([1,2,3,3],[1,2,3,4])