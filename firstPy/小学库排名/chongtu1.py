#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys,json,oss2,hashlib,traceback,os,MySQLdb,string,chardet
reload(sys)
sys.setdefaultencoding('utf-8')
conn = MySQLdb.connect(host="127.0.0.1",user="zhanqun",passwd="wdlPD40xjO5",db="zhanqun", charset="utf8", port = 3305)
cursor = conn.cursor()
auth = oss2.Auth('BPvWuBAlq5rxM3qm', '1EMB2SelO9EQaue3E3xN09zJajB4Dm')
bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'genshuixue-public')
def get_image(filename):
      try:
          dstfilename = 'zhanqun/xiaoxue/' + hashlib.md5(filename).hexdigest() + '.' + filename.split('.')[-1]
          bucket.put_object_from_file(dstfilename, filename)
          return 'http://file.gsxservice.com/' + dstfilename
      except:
          traceback.print_exc()
          return None

for file in os.listdir('/Users/bjhl/Documents/imgs_edit'):
    if not file.endswith('.jpg'):
        continue
    id = file.split('.')[0].strip()
    #print int(id)
    new_display_image = get_image('/Users/bjhl/Documents/imgs_edit/'+file)
    print new_display_image
    #break
    sql = "update primary_school_info set display_image ='%s' where id=%s" % (new_display_image,id)
    cursor.execute(sql)
    conn.commit()