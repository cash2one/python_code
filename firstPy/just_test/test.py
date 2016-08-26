#ecoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
print time.time()
s = '1、'
print '%s' % s[1]

print '--' == '--asdasdas'[0:2]
import os
#os.system("kill -9 `ps -ef | grep Google | awk '{print $2}'`")
s1 = '　　澳洲留学学费'
s2 = '　　澳洲留学前期费用'
print s1[0:2]
print str(s1[0:2])
print s1[0:2] == s2[0:2]
s3 = 's'
s4 = s3.replace('s','ss')
print s3, s4
import  urllib
a= '\xE8\xBF\x87\xE5\x8E'
print urllib.unquote(a).decode('utf-8', 'replace')+ '11'
add_words = [
    'bj',
    'sh',
    'sd',
    'js',
    'zj',
    'ah',
    'jl',
    'fj',
    'gd',
    'gx',
    'hn',
    'tj',
    'hb',
    'hlj',
    'sx',
    'gs',
    'hu',
    'hn',
    'he',
    'sc',
    'cq',
    'yn',
    'gz',
    'xz',
    'nx',
    'xj',
    'qh',
    'sx',
    'ln',
    'jx',
    'nmg',
]