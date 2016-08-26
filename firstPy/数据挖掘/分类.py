#ecoding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
print len(target)

t = zeros(len(target))
#print t
t[target == 'setosa'] = 1
t[target == 'versicolor'] = 2
t[target == 'virginica'] = 3

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(data,t) # training on the iris dataset
print classifier.predict(data[0])
print t[0]
