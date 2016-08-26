#ecoding:utf-8
import urllib
import sys,re
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
# html = urllib.urlopen('http://news.21cnjy.com/A/130/114/V88684.shtml').read()
# for each in  pq(html).find('#article_content table tr').items():
#     print "u'"+each.text().split()[1]+"': u'"+each.text().split()[0]+"',"


# html = urllib.urlopen('http://mt.sohu.com/20150731/n417906147.shtml').read()
# for each in  pq(html).find('div[itemprop="articleBody"] > p').items():
#     if each.find('*'):
#         continue
#     print "u'"+each.text().split('、')[1]+"': u'"+each.text().split('、')[0]+"',"

#html = urllib.urlopen('http://xuexiao.chazidian.com/news92116/').read()
#for each in  pq(html).find('#print_content > p:gt(1)').items():
# for each in  pq(html).find('#print_content > p').items():
#     if each.find('*'):
#         continue
#     #print each.text()
#     if re.match(r'[0-9]+',each.text()):
#         print "u'"+re.sub(r'[0-9]+','',each.text())+"': u'"+re.match(r'[0-9]+',each.text()).group()+"',"
# for line in open('/Users/bjhl/Documents/sjz_dict'):
#     print "u'"+line.split()[1]+"': u'"+line.split()[0]+"',"
# for j in range(1,2):
#     j = '0'+str(j) if len(str(j))==1 else str(j)
i = 0
for p in range(1,5):
    p = str(p)
    #url = 'http://xuexiao.51sxue.com/slist/?o=&t=2&areaCodeS=4403'+j+'&level=&sp=&score=&order=&areaS=%B9%E3%D6%DD%CA%D0&searchKey=&page='+p
    url = 'http://xuexiao.51sxue.com/slist/?t=2&areaCodeS=6301&page='+p
    html = urllib.urlopen(url).read()
    for each in  pq(html).find('#dsadas').items():
        # if each.find('*'):
        #     continue
        i += 1
        print "u'"+each.text()+"': u'"+str(i)+"',"
    #print pq(html).find('body').html()
