#ecoding:utf-8
import re

date = u'于(2006年9月1日)-2007年8月31日出生且身心健康的适龄儿童。'
date = re.sub(u'[0-9]{4}年',u'2009年',date,re.S)
date = re.sub(u'-[0-9]{4}年',u'-2010年',date,re.S)
print date
print re.search(u'[0-9]{4}年',date,re.S).group()
print len(re.findall(u'[0-9]{4}年',date,re.S))
print re.findall(u'[0-9]{4}年',date,re.S)[0]