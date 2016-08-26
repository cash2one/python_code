# -*- coding: UTF-8 -*-
def power(x):
    return x*x
print power(3)
#函数可以赋值给变量
d = power
print d(4)
#匿名函数,或者叫做lambda函数,它没有名字,只有参数和表达式:
dd = lambda x :  x + 1
print dd(3)
a = [1,2,3,4]
#lambda最大的用处是用作实参:
def iter(func, list):
    ret = [];
    for temp in list:
        ret.append(func(temp))
    return  ret
print iter(lambda x: x+1, a)
print iter(power, a)
print iter
#help('print')