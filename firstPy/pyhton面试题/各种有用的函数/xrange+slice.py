#ecoding:utf-8
l = range(10)
print l[::2]
print l[::-1]

print l[slice(3,5)]
#而xrange则不会直接生成一个list，而是每次调用返回其中的一个值：
ll = xrange(10)
print l
print list(ll)