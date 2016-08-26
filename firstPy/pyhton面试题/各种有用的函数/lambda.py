f = lambda x,y,z:x+y+z
print f(1,2,4)

def a(x):
    return lambda y:x+y
b = a(1)
print b(3)