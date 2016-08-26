#ecoding:utf8

import urllib2
url = 'http://aima.cs.berkeley.edu/data/iris.csv'
#u = urllib2.urlopen(url).read()
dir = '/Users/bjhl/Documents/data_mining/'
filename = 'iris.csv'
# with open(dir+filename,'w') as fw:
#     fw.write(u)
#     fw.flush()
#print u
from numpy import genfromtxt, zeros
#read the first 4 columns
#data =  genfromtxt(url,delimiter=',',usecols=(0,1,2,3))
data = genfromtxt(dir+filename,delimiter=',',usecols=(0,1,2,3))
print data.shape
print type(data)
# read the fifth column
#target = genfromtxt(url,delimiter=',',usecols=(4),dtype=str)
target = genfromtxt(dir+filename,delimiter=',',usecols=(4),dtype=str)
print target.shape
print type(target)


# from pylab import plot,show
# plot(data[target=='setosa',0],data[target=='setosa',2],'bo')
# plot(data[target=='versicolor',0],data[target=='versicolor',2],'ro')
# plot(data[target=='virginica',0],data[target=='virginica',2],'go')
# show()

from pylab import figure, subplot, hist, xlim, show
xmin = min(data[:,0])
xmax = max(data[:,0])
print xmax,xmin
print figure()
subplot(411) # distribution of the setosa class (1st, on the top)
hist(data[target=='setosa',0],color='b',alpha=.7)
xlim(xmin,xmax)
subplot(412) # distribution of the versicolor class (2nd)
hist(data[target=='versicolor',0],color='r',alpha=.7)
xlim(xmin,xmax)
subplot(413) # distribution of the virginica class (3rd)
hist(data[target=='virginica',0],color='g',alpha=.7)
xlim(xmin,xmax)
subplot(414) # global histogram (4th, on the bottom)
hist(data[:,0],color='y',alpha=.7)
xlim(xmin,xmax)
show()