#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class stu:
    age = 0;
    sex = '男'
    def __init__(self,age,sex):
        self.age = age
        self.sex = sex

b = stu(2,'女')
def test(x):
    x.age = 3
    x.sex = '妖'
    x = b

a = stu(1,'男')
print a.age,a.sex
# test(a);
# print a.age,a.sex
a = b
print a.age,a.sex
print b.age,b.sex
b.age = 4
b.sex = '男'
print a.age,a.sex
print b.age,b.sex
a.age = 5
a.sex = '男'
print a.age,a.sex
print b.age,b.sex

