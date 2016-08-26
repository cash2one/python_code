#ecoding:utf8
def foo(x):
    return x*x

from multiprocessing.dummy import Pool
p = Pool(processes=5)
import time
start = time.time()
p.map(foo,range(100000000))
end =time.time()
print end-start