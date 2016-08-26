#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import urllib2
import chardet,urllib
reload(sys)
sys.setdefaultencoding("utf-8")
#直接通过找到的接口爬取
def process():
        for i in range(0,1665):
            try:
                content = urllib2.urlopen("http://wx.233.com/search/UserCenter/task/Wenda/AskList.ashx?Act=GetAskList&ClassID=0&ClassIDStr=&Page=0&AskType=2&PageSize=15&Types=NaN&OrderBy=addtime&types0=0&types5=0&types1=0&types3=0&_=1469503906564",timeout=5).read()
            except:
                traceback.print_exc()
                continue
            _dict = json.loads(content)
            if _dict.has_key('AskList'):
                for each in _dict['AskList']:
                    if each.has_key('AskID') and each.has_key('Content'):
                        print each['AskID']
                        print chardet.detect(str(each['Content']))
                        print urllib.unquote(each['Content']).decode('utf-8', 'replace')
                        print str(each['Content']).decode('utf-8').encode('utf8')
            break

if __name__ == '__main__':
    process()