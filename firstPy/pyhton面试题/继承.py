#ecoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class Parent(object):
    x = 1
class Child1(Parent):
    pass
class Child2(Parent):
    pass
print Parent.x, Child1.x, Child2.x


Child1.x = 2
print Parent.x, Child1.x, Child2.x
Parent.x = 3
print Parent.x, Child1.x, Child2.x
#如果一个变量的名字没有在当前类的字典中发现，将搜索祖先类（比如父类）直到被引用的变量名被找到
# （如果这个被引用的变量名既没有在自己所在的类又没有在祖先类中找到，会引发一个 AttributeError 异常 ）。

c1 = Child1()
print type(c1)
print isinstance(c1, Child1)
