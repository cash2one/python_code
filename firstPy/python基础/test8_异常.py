# -*- coding: UTF-8 -*-
# def func(level):
#     if level < 1:
#         raise  Exception("invalid",level)
# try:
#     func(0)
# except "":
#     print 1
# else:
#     print 2
class Networkerror(RuntimeError):
    #def __init__类的构造方法
    #用途:初始化实例的值.这些值一般要供其他方法调用
    #要求:只初始化值,不要返回值(就是别用return)
    def __init__(self1, arg):
        self1.args = arg


try:
    raise Networkerror("Bad hostname")
except Networkerror,e:
    print e.args