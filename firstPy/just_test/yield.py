def g(n):
    for i in range(n):
        yield i **2
def t(n):
    return n+1
for i in g(5):
    print t(i),":",