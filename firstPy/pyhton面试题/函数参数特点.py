#ecoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def cli(ctx,**kwargs ):
    print ctx
    for k in kwargs:
        print k, kwargs[k]
    for k, v in kwargs.iteritems():
        print k,v
cli(ctx=1,k1=2,k2=3)



def cli2(ctx,*args ):
    print ctx
    for k in args:
        print k

cli2(1,2,3)