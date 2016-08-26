#ecoding:utf8
class P:
    def __init__(self):
        print 'p ok'

class C(P):
    #pass
    #如果要继承父函数的构造方法,就不写
    def __init__(self):
        P.__init__(self)


p1 = P()
c1 = C()
