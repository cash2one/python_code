#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import six
from six import iteritems
from six import itervalues
import mysql.connector

class BaseDB:

    '''
    BaseDB
    dbcur should be overwirte
    '''
    __tablename__ = None
    placeholder = '%s'

    @staticmethod
    def escape(string):
        return '`%s`' % string

    @property
    def dbcur(self):
        raise NotImplementedError

    def _execute(self, sql_query, values=[]):
        dbcur = self.dbcur
        dbcur.execute(sql_query, values)
        return dbcur

    def _select(self, tablename=None, what="*", where="", where_values=[], offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #logger.debug("<sql: %s>", sql_query)

        for row in self._execute(sql_query, where_values):
            yield row

    def _select2dic(self, tablename=None, what="*", where="", where_values=[],
                    order=None, offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order:
            sql_query += ' ORDER BY %s' % order
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #logger.debug("<sql: %s>", sql_query)

        dbcur = self._execute(sql_query, where_values)
        fields = [f[0] for f in dbcur.description]

        for row in dbcur:
            yield dict(zip(fields, row))

    def _replace(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join(self.escape(k) for k in values)
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "REPLACE INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _insert(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join((self.escape(k) for k in values))
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "INSERT INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _update(self, tablename=None, where="1=0", where_values=[], **values):
        tablename = self.escape(tablename or self.__tablename__)
        _key_values = ", ".join([
            "%s = %s" % (self.escape(k), self.placeholder) for k in values
        ])
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)
        #print ("<sql: %s>", sql_query)

        return self._execute(sql_query, list(itervalues(values)) + list(where_values))

    def _delete(self, tablename=None, where="1=0", where_values=[]):
        tablename = self.escape(tablename or self.__tablename__)
        sql_query = "DELETE FROM %s" % tablename
        if where:
            sql_query += " WHERE %s" % where
        #logger.debug("<sql: %s>", sql_query)

        return self._execute(sql_query, where_values)


class DB(BaseDB):
    __tablename__ = "primary_school_info"

    def __init__(self):
        config = {'host': '127.0.0.1',  # 默认127.0.0.1
                  'user': 'zhanqun',
                  'password': 'wdlPD40xjO5',
                  'port': 3305,  # 默认即为3306
                  'database': 'zhanqun',
                  'charset': 'utf8' ,
                  'autocommit' : True
                  }

        self.conn = mysql.connector.connect(**config)
        self.database_name = 'zhanqun'

    @property
    def dbcur(self):
        try:
            if self.conn.unread_result:
                self.conn.get_rows()
            return self.conn.cursor()
        except (mysql.connector.OperationalError, mysql.connector.InterfaceError):
            self.conn.ping(reconnect=True)
            self.conn.database = self.database_name
            return self.conn.cursor()



db = DB()
sh_dict = {
u'上海小学': u'1',
u'上海师范大学第一附属小学': u'2',
u'上海市实验小学': u'3',
u'上海市蓬莱路第二小学': u'4',
u'上海静安区一师附小': u'5',
u'上海静安区第一中心小学': u'6',
u'上海卢湾区第一中心小学': u'7',
u'上海市卢湾区第二中心小学': u'8',
u'上海江苏路第五小学': u'9',
u'上海愚园路第一小学': u'10',
u'上海虹口区第三中心小学': u'11',
u'上海崇明路小学': u'12',
u'上海武宁路小学': u'13',
u'上海中山北路第一小学': u'14',
u'上海复旦大学附属小学': u'15',
u'上海闸北区实验小学': u'16',
u'上海新世界实验小学': u'17',
u'上海福山外国语小学': u'18',
u'上海闵行区实验小学': u'19',
u'上海闵行区中心小学': u'20',
u'上海红星小学': u'21',
u'上海宝山区宝山实验小学': u'22',
u'上海松江区实验小学': u'23',
u'上海市世界外国语小学': u'24',
u'上海杨浦小学': u'25',
u'上海市复兴东路第三小学': u'26',
u'上海市黄浦区第一中心小学': u'27',
u'上海民办打一外国语小学': u'28',
u'上海市第一实验小学': u'29',
u'上海庆华小学': u'30',
u'上海新时代小学(浦三路校区)': u'31',
u'上海颜安小学': u'32',
u'上海杨浦区世界小学': u'33',
u'上海明达小学': u'34',
u'上海洛川东路小学': u'35',
u'上海杨思小学': u'36',
u'上海青浦区凤溪小学': u'37',
u'上海青浦区华新小学': u'38',
u'上海广育小学': u'39',
u'上海梅溪小学': u'40',
u'上海徐浦小学': u'41',
u'上海宝山路小学': u'42',
u'上海明山小学': u'43',
u'上海安顺路小学': u'44',
u'上海止园路小学': u'45',
u'上海厦门路小学': u'46',
u'上海长宁路小学': u'47',
u'上海绿地小学': u'48',
u'上海向红小学': u'49',
u'上海永清路小学': u'50',
u'上海中原路小学(中原路校区)': u'51',
u'上海市裘锦秋实验学校': u'52',
u'上海新昌路小学': u'53',
u'上海黎明小学': u'54',
u'上海新武宁小学': u'55',
u'上海文庙路小学': u'56',
u'上海浦明师范学校附属小学': u'57',
u'上海碧江路小学': u'58',
u'上海云台小学': u'59',
u'上海光明小学': u'60',
u'上海万荣小学': u'61',
u'上海青浦区徐泾小学': u'62',
u'上海淞虹路小学': u'63',
u'上海丹徒路小学': u'64',
u'上海浦明师范附属小学(东城校区)': u'65',
u'上海平南小学': u'66',
u'上海瑞金二路小学': u'67',
u'上海民办丽英小学': u'68',
u'上海景凤路小学': u'69',
u'上海丽江小学': u'70',
u'上海东方小学': u'71',
u'上海梧桐路小学': u'72',
u'上海樱花园小学': u'73',
u'上海乌镇路小学': u'74',
u'上海和田路小学': u'75',
u'上海金英小学': u'76',
u'上海南桥小学': u'77',
u'上海广中路小学': u'78',
u'上海树德小学': u'79',
u'上海徐汇区世界小学': u'80',
u'上海竹园小学(张杨校区)': u'81',
u'上海民办弘梅小学': u'82',
u'上海市东小学': u'83',
u'上海东沟小学': u'84',
u'上海海桐小学(东城校区)': u'85',
u'上海普通小学': u'86',
u'上海六一小学': u'87',
u'上海红旗小学': u'88',
u'上海香山小学': u'89',
u'上海控江二村小学(本部)': u'90',
u'上海园南小学': u'91',
u'上海四川南路小学': u'92',
u'上海平阳小学': u'93',
u'上海育童小学': u'94',
u'上海白玉兰小学': u'95',
u'上海逸夫小学': u'96',
u'上海光启小学': u'97',
u'上海真光小学': u'98',
u'上海华林小学': u'99',
}
sz_dict1 = {
u'深圳北师大南山附小': u'1',
u'深圳南山外国语学校科苑小学': u'2',
u'深圳市南山小学': u'3',
u'深圳市南山区育才一小': u'4',
u'深圳市南山区育才二小': u'5',
u'深圳市海滨实验小学(愉康部)': u'6',
u'深圳市华侨城小学': u'7',
u'深圳市南山区海湾小学': u'8',
u'深圳市南头城小学': u'9',
u'深圳市南山区珠光小学': u'10',
u'深圳市南山区西丽小学': u'11',
u'深圳市南山区南油小学': u'12',
u'深圳市南山区沙河小学': u'13',
u'深圳市南山区松坪学校小学部': u'14',
u'深圳市南山区松坪第二小学': u'15',
u'深圳市南山实验学校(南头小学部)': u'16',
u'深圳市南山区松坪学校': u'17',
u'深圳市平山小学': u'18',
u'深圳市学府小学(海文部)': u'19',
u'深圳市蛇口学校小学部': u'20',
u'深圳市南山区桃源小学': u'21',
u'深圳市南山区大新小学': u'22',
u'深圳市南山区向南小学': u'23',
u'深圳南山同乐学校小学部': u'24',
u'中央教育科学研究所南山附属学校(央校)': u'25',
u'深圳市南山区卓雅小学': u'26',
u'深圳市南山区月亮湾小学': u'27',
u'深圳市后海小学': u'28',
u'深圳市南山育才四小': u'29',
u'圳市南山区白芒小学': u'30',
u'深圳实验学校小学部': u'1',
u'深圳市园岭小学': u'2',
u'深圳市荔园小学北校区': u'3',
u'深圳市百花小学': u'4',
u'深圳市福田区莲花小学': u'5',
u'深圳市华富小学': u'6',
u'深圳市梅丽小学': u'7',
u'深圳市荔园小学南校区': u'8',
u'深圳市福田区荔园外国语小学东校区': u'9',
u'深圳市天健小学': u'10',
u'深圳市竹园小学': u'11',
u'深圳市南华小学': u'12',
u'深圳外国语学校东海附属小学': u'13',
u'深圳市福田区荔园外国语小学西校区': u'14',
u'深圳市福民小学': u'15',
u'深圳市荔轩小学': u'16',
u'深圳市益强小学': u'17',
u'深圳市福田保税区外国语小学': u'18',
u'深圳市福田区益田小学': u'19',
u'深圳市福田区丽中小学': u'20',
u'深圳市福南小学': u'21',
u'深圳市福田区岗厦小学': u'22',
u'深圳市众孚小学': u'23',
u'深圳市福田区南园小学': u'24',
u'深圳市福田区景田小学': u'25',
u'深圳市福田区福新小学': u'26',
u'深圳市福田区狮岭小学': u'27',
u'深圳市福田区景秀小学': u'28',
u'深圳市福田区下沙小学': u'29',
u'深圳市福田区福强小学': u'30',
u'深圳市宝安实验学校(小学部)': u'1',
u'深圳市南山区西丽福华小学': u'2',
u'深圳市宝安区宝民小学': u'3',
u'深圳市西乡街道中心小学': u'4',
u'深圳市石岩公学小学部': u'5',
u'深圳市宝安区建安小学': u'6',
u'深圳市民治小学': u'7',
u'深圳市弘雅小学': u'8',
u'深圳市天骄小学': u'9',
u'深圳清华实验学校小学部': u'10',
u'深圳市宝安区宝城小学': u'11',
u'深圳市宝安区天骄小学': u'12',
u'深圳市宝安区滨海小学': u'13',
u'深圳市宝安中学附属小学': u'14',
u'深圳宝安标尚学校': u'15',
u'深圳宝安崇文学校': u'16',
u'深圳宝安陶园中英文实验学校': u'17',
u'深圳市宝安外国语学校': u'18',
u'深圳市光明新区公明长圳小学': u'19',
u'深圳市光明新区公明田寮小学': u'20',
u'深圳市宝安区光明小学': u'21',
u'深圳龙华中英文实验学校': u'22',
u'深圳市宝安区黄田小学': u'23',
u'深圳市宝安区福永中心小学': u'24',
u'深圳市宝安区塘尾万里学校小学部': u'25',
u'深圳市龙华中心小学': u'26',
u'深圳市松岗第一小学': u'27',
u'深圳市宝安区燕山学校小学部': u'28',
u'深圳市宝安区松岗街道东方小学': u'29',
u'深圳市宝安区荣根学校': u'30',
u'深圳市翠竹小学(深圳市翠竹外国语实验学校)': u'1',
u'深圳市螺岭外国语实验学校(原螺岭小学)': u'2',
u'深圳小学': u'3',
u'深圳市罗湖区红岭小学': u'4',
u'深圳市罗湖小学': u'5',
u'深圳市罗湖区水库小学': u'6',
u'深圳市翠北小学': u'7',
u'深圳市罗湖区北斗小学': u'8',
u'深圳市翠茵小学': u'9',
u'深圳市桂园小学': u'10',
u'深圳市罗湖区滨河小学': u'11',
u'深圳市罗湖区洪湖小学': u'12',
u'深圳市锦田小学': u'13',
u'深圳市百仕达小学': u'14',
u'深圳南山外国语学校文华学校小学': u'15',
u'深圳市向西小学': u'16',
u'深圳市南湖小学': u'17',
u'深圳市罗湖区笋岗小学': u'18',
u'深圳市怡景小学': u'19',
u'深圳市靖轩小学': u'20',
u'深圳市布心小学': u'21',
u'深圳市罗湖区东晓小学': u'22',
u'深圳市湖贝小学': u'23',
u'深圳市新港小学': u'24',
u'深圳市罗湖区罗芳小学': u'25',
u'深圳市碧波小学': u'26',
u'深圳市景贝小学': u'27',
u'深圳市罗湖区莲南小学': u'28',
u'深圳市明珠中英文小学': u'29',
u'深圳市大望学校': u'30',
}
sz_dict = {
u'深圳荔园小学': u'1',
u'深圳实验学校小学': u'2',
u'深圳螺岭小学': u'3',
u'深圳翠竹小学': u'4',
u'深圳园岭小学': u'5',
u'深圳华富小学': u'6',
u'深圳小学': u'7',
u'深圳锦田小学': u'8',
u'深圳水库小学': u'9',
u'深圳百花小学': u'10',
u'深圳保税区小学': u'11',
u'深圳百仕达小学': u'12',
u'深圳南山实验学校': u'13',
u'深圳南头城小学': u'14',
u'深圳碧波小学': u'15',
u'深圳景田小学': u'16',
u'深圳南油小学': u'17',
u'深圳罗湖小学': u'18',
u'深圳红岭小学': u'19',
u'深圳培英文武实验学校': u'20',
u'深圳东升学校': u'21',
u'深圳翠茵小学': u'22',
u'深圳梅园小学': u'23',
u'深圳新秀小学': u'24',
u'深圳莲花小学': u'25',
u'深圳侨香学校': u'26',
u'深圳福田小学': u'27',
u'深圳众孚小学': u'28',
u'深圳华府小学': u'29',
u'深圳绿洲小学': u'30',
u'深圳嘉联学校': u'31',
u'深圳横岗中心小学': u'32',
u'深圳华城学校': u'33',
u'深圳大唐小学': u'34',
u'深圳梅丽小学': u'35',
u'深圳官湖学校': u'36',
u'深圳坂田小学': u'37',
u'深圳钟屋小学': u'38',
u'深圳景莲小学': u'39',
u'深圳南园小学': u'40',
u'深圳精华学校': u'41',
u'深圳学府小学': u'42',
u'深圳下李朗小学': u'43',
u'深圳上沙小学': u'44',
u'深圳碧海小学': u'45',
u'深圳北师大附小': u'46',
u'深圳永联小学': u'47',
u'深圳牛栏前学校': u'48',
u'深圳福新小学': u'49',
u'深圳英才小学': u'50',
u'深圳大新小学': u'51',
u'深圳春蕾小学': u'52',
u'深圳上南学校': u'53',
u'深圳横朗小学': u'54',
u'深圳龙岭学校': u'55',
u'深圳英才学校': u'56',
u'深圳鹏达学校': u'57',
u'深圳福民小学': u'58',
u'深圳实验学校南头小学': u'59',
u'深圳鹤围学校': u'60',
u'深圳宝安区公明第一小学': u'61',
u'深圳景秀小学': u'62',
u'深圳上步小学': u'63',
u'深圳博文学校': u'64',
u'深圳黄埔小学': u'65',
u'深圳华升学校': u'66',
u'深圳兴围小学': u'67',
u'深圳才德小学': u'68',
u'深圳西乡中心小学': u'69',
u'深圳龙岗区坪山镇第二小学': u'70',
u'深圳翠华小学': u'71',
u'深圳流塘小学': u'72',
u'深圳水田小学': u'73',
u'深圳皇岗小学': u'74',
u'深圳兴文学校': u'75',
u'深圳明星学校': u'76',
u'深圳红桂小学': u'77',
u'深圳陶园中英文实验学校': u'78',
u'深圳塘头小学.': u'79',
u'深圳陶园中英文学校': u'80',
u'深圳宝城小学': u'81',
u'深圳南山小学': u'82',
u'深圳平安里学校': u'83',
u'深圳文德学校': u'84',
u'深圳坪西小学': u'85',
u'深圳径贝小学': u'86',
u'深圳文成学校': u'87',
u'深圳中山学校': u'88',
u'深圳南芳学校': u'89',
u'深圳蛇口小学': u'90',
u'深圳辅城坳小学': u'91',
u'深圳北京景山学校分校': u'92',
u'深圳天成学校': u'93',
u'深圳梧桐学校': u'94',
u'深圳竹林小学': u'95',
u'深圳石厦学校小学部': u'96',
u'深圳樟树布小学': u'97',
u'深圳弘雅小学': u'98',
u'深圳德兴小学': u'99',

}
gz_dict = {
u'广州天河区华阳小学': u'1',
u'广州东风东路小学': u'2',
u'广州东山培正小学': u'3',
u'广州协和小学': u'4',
u'广州越秀区旧部前小学': u'5',
u'广州越秀区朝天小学': u'6',
u'广州小北路小学': u'7',
u'广州东风西路小学（东风西小学）': u'8',
u'广州同福中路第一小学（同福中路一小）': u'9',
u'广州万松园小学': u'10',
u'广州海珠区实验小学': u'11',
u'广州沙面小学': u'12',
u'广州天河区体育东路小学': u'13',
u'广州华南师范大学附属小学（华师附小）': u'14',
u'广州怡园小学': u'15',
u'广州市黄埔区荔园小学': u'16',
u'广州华南理工大学附属小学': u'17',
u'广州侨乐小学': u'18',
u'广州华南师范大学附属小学': u'19',
u'广州桂花岗小学': u'20',
u'广州滨江东路第二小学': u'21',
u'广州五一小学': u'22',
u'广州三滘小学': u'23',
u'广州开发区第一小学': u'24',
u'广州建设六马路小学': u'25',
u'广州员村第五小学': u'26',
u'广州菩提路小学': u'27',
u'广州昌岗中路小学': u'28',
u'广州黄花小学': u'29',
u'广州文德路小学': u'30',
u'广州客村小学': u'31',
u'广州中星小学': u'32',
u'广州新港中路小学': u'33',
u'广州镇泰实验小学': u'34',
u'广州八旗二马路小学': u'35',
u'广州东风东路小学东风广场校区': u'36',
u'广州宝贤大街小学': u'37',
u'广州宝玉直街小学': u'38',
u'广州复甦小学': u'39',
u'广州官溪小学': u'40',
u'广州义沙小学': u'41',
u'广州东导小学': u'42',
u'广州学培纪念学校': u'43',
u'广州迁岗小学': u'44',
u'广州罗洞小学': u'45',
u'广州长沙小学': u'46',
u'广州顺河小学': u'47',
u'广州黄麻小学': u'48',
u'广州市白云区龙湖小学': u'49',
u'人和镇蚌湖第一小学': u'50',
u'广州陈涌小学': u'51',
u'广州十八甫南小学': u'52',
u'广州新星小学': u'53',
u'广州江夏小学': u'54',
u'广州骏景小学': u'55',
u'广州东联小学建业一路校区': u'56',
u'广州乐贤坊小学': u'57',
u'广州环山小学': u'58',
u'广州沙凤小学': u'59',
u'广州大云小学': u'60',
u'广州莲中心小学': u'61',
u'广州东莞小学': u'62',
u'广州同源小学': u'63',
u'广州西华路小学': u'64',
u'广州石厦小学': u'65',
u'增城山村小学': u'66',
u'广州双井街小学': u'67',
u'广州塘田小学': u'68',
u'广州公益小学': u'69',
u'广州三沙小学': u'70',
u'广州长兴小学': u'71',
u'广州骏苗小学': u'72',
u'广州市白云区人和小学': u'73',
u'广州六二三小学': u'74',
u'广州江南大道南小学': u'75',
u'广州龙涛学校': u'76',
u'广州文峰小学': u'77',
u'广州梅园西路小学(北校区)': u'78',
u'广州凌塘小学': u'79',
u'增城市新塘镇永和小学': u'80',
u'广州瀛洲小学': u'81',
u'广州均和小学': u'82',
u'广州瑞宝小学': u'83',
u'广州孟田小学': u'84',
u'广州山田小学': u'85',
u'广州钟岭小学': u'86',
u'广州东川路第二小学': u'87',
u'广州大坳小学': u'88',
u'广州长湴小学': u'89',
u'湴湄镇泰小学': u'90',
u'广州水濂小学': u'91',
u'广州新同丰小学': u'92',
u'广州江埔镇中心小学': u'93',
u'广州石头小学': u'94',
u'广州执信南路小学': u'95',
u'广州屏山小学': u'96',
u'广州江埔小学': u'97',
u'广州黄登小学': u'98',
u'广州元田小学': u'99',
}
hz_dict = {
u'杭州天长小学': u'1',
u'杭州胜利小学': u'2',
u'杭州师范大学第一附属小学': u'3',
u'杭州求是小学': u'4',
u'杭州紫阳小学': u'5',
u'杭州东岳小学': u'6',
u'杭州学军小学': u'7',
u'杭州孩儿巷小学': u'8',
u'杭州笕桥小学': u'9',
u'杭州新华小学': u'10',
u'杭州大关苑第二小学': u'11',
u'临安临天辅导小学': u'12',
u'杭州近江小学': u'13',
u'杭州育才实验小学': u'14',
u'杭州市留下小学': u'15',
u'杭州市余杭区崇贤镇第一中心小学': u'16',
u'杭州宏图中心小学': u'17',
u'径游中心小学': u'18',
u'建德钦堂乡庄丰小学': u'19',
u'建德三岩小学': u'20',
u'杭州树人小学': u'21',
u'杭州兴旺小学': u'22',
u'杭州湘湖师范附属小学': u'23',
u'富阳新桥完全小学': u'24',
u'杭州江南实验小学': u'25',
u'杭州学军小学(紫金校区)': u'26',
u'萧山义桥实验学校': u'27',
u'余杭市余杭镇太炎小学': u'28',
u'萧山区坎山镇中心小学': u'29',
u'党湾镇第一小学': u'30',
u'萧山区临浦镇第四小学': u'31',
u'杭州北秀小学': u'32',
u'杭州新塘中心小学': u'33',
u'杭州长寿桥小学长青分校再行巷校区': u'34',
u'富阳鹿山街道驯雉完全小学': u'35',
u'杭州盛东小学': u'36',
u'杭州永兴中心小学': u'37',
u'富阳窈口乡永兴小学': u'38',
u'富阳富春第二小学': u'39',
u'杭州通济中心小学': u'40',
u'杭州艮山路小学': u'41',
u'杭州华藏寺巷小学': u'42',
u'杭州圆通小学': u'43',
u'杭州求是小学(星洲校区)': u'44',
u'杭州开元小学': u'45',
u'杭州沿江小学': u'46',
u'富阳平畈小学': u'47',
u'杭州荣星小学': u'48',
u'余杭市崇贤镇第二小学': u'49',
u'杭州买鱼桥小学': u'50',
u'桐庐镇洋洲仁智小学': u'51',
u'富阳真佳溪小学': u'52',
u'杭州彩虹城小学': u'53',
u'杭州东塘中心小学': u'54',
u'杭州胜稼小学': u'55',
u'杭州五常中心小学': u'56',
u'桐庐县旧县镇中心小学': u'57',
u'富阳羊家埭小学': u'58',
u'杭州新围中心小学': u'59',
u'萧山区瓜沥镇第三小学': u'60',
u'杭州赭山中心小学': u'61',
u'杭州求是小学(竞舟校区)': u'62',
u'萧山区进化镇第三小学': u'63',
u'杭州盈丰中心小学': u'64',
u'杭州现代实验小学': u'65',
u'杭州袁浦乡中心小学': u'66',
u'杭州黄龙洞小学': u'67',
u'杭州五杭中心小学': u'68',
u'杭州浙江省教育厅教研室附属小学': u'69',
u'杭州文一路小学': u'70',
u'杭州荻浦小学': u'71',
u'横村镇小学': u'72',
u'杭州明珠教育集团学校明志校区': u'73',
u'建德市新安江第三小学': u'74',
u'杭州西湖区转塘镇中心小学': u'75',
u'杭州宁围镇中心小学': u'76',
u'杭州长河镇中心小学': u'77',
u'杭州天成小学': u'78',
u'杭州市西兴实验小学': u'79',
u'萧山区靖江镇第二小学': u'80',
u'杭州杨绫子学校': u'81',
u'杭州临目小学': u'82',
u'新登镇中心小学': u'83',
u'杭州聋人学校': u'84',
u'杭州绿城育华小学': u'85',
u'杭州双溪中心小学': u'86',
u'杭州经济技术开发区阳光小学': u'87',
u'杭州六堡小学': u'88',
u'杭州角美第中心小学': u'89',
u'杭州省府路小学': u'90',
u'杭州拱宸桥小学左岸校区': u'91',
u'杭州龙川小学': u'92',
u'余杭市勾庄镇中心小学': u'93',
u'杭州市袁浦小学': u'94',
u'杭州大关苑第三小学': u'95',
u'塘栖镇第一小学': u'96',
u'杭州洪圻村小学': u'97',
u'淳安县汾口镇小学': u'98',
u'建德洋溪新华小学': u'99',
}
tj_dict = {
u'天津市实验小学': u'1',
u'天津和平区中心小学': u'2',
u'天津鞍山道小学': u'3',
u'天津昆鹏小学': u'4',
u'天津逸阳小学': u'5',
u'天津育婴里小学': u'6',
u'天津万全道小学': u'7',
u'天津河东实验小学': u'8',
u'天津上海道小学': u'9',
u'天津师范大学附属小学': u'10',
u'天津师范大学第二附属小学': u'11',
u'天津求真小学': u'12',
u'天津扶轮小学': u'13',
u'天津东方小学': u'14',
u'天津南开区中营小学': u'15',
u'天津模范小学': u'16',
u'天津师范学校附属小学': u'17',
u'天津双树小学': u'18',
u'天津河东区一中心小学': u'19',
u'天津北环路小学': u'20',
u'天津新会道小学': u'21',
u'天津小集中心小学': u'22',
u'天津沿河小学': u'23',
u'天津小港学校': u'24',
u'天津市红桥区实验小学': u'25',
u'天津实验求真小学': u'26',
u'天津陈庄小学': u'27',
u'天津六一小学': u'28',
u'天津北马中心小学': u'29',
u'天津芮家庄小学': u'30',
u'天津于少屯中心小学': u'31',
u'天津王口镇第四中心小学': u'32',
u'天津北城路小学': u'33',
u'天津市静海县杨成庄乡董庄窠小学': u'34',
u'天津穿芳峪乡第一中心小学': u'35',
u'天津桃李园小学': u'36',
u'天津市宝坻区高家庄镇三岔口中心小学': u'37',
u'天津市大港第四小学': u'38',
u'天津塘沽区实验小学': u'39',
u'天津湘江道小学': u'40',
u'天津安家务小学': u'41',
u'天津港狮学校': u'42',
u'天津唐头庄中心小学': u'43',
u'天津大新中心小学': u'44',
u'天津尤张堡小学': u'45',
u'天津仓前庄中心小学': u'46',
u'天津市宝坻区大钟庄中心小学': u'47',
u'天津高中心小学': u'48',
u'天津大黄堡乡四高庄小学': u'49',
u'天津满意庄学校': u'50',
u'天津清官完全小学': u'51',
u'天津越秀园小学': u'52',
u'天津张子铺中心小学': u'53',
u'天津黄沙务小学': u'54',
u'天津大三河小学': u'55',
u'天津西堤头小学': u'56',
u'天津台头镇第一小学': u'57',
u'天津胡连庄小学': u'58',
u'天津穿芳峪乡果香峪中心小学': u'59',
u'天津江南寄宿小学': u'60',
u'天津何庄子小学': u'61',
u'天津小邀铺小学': u'62',
u'天津梁头中心小学': u'63',
u'天津东赵乡南辛庄小学': u'64',
u'天津北王庄中心小学': u'65',
u'天津造甲城中心小学': u'66',
u'天津八里庄完全小学': u'67',
u'天津二光小学': u'68',
u'天津大?上中心小学': u'69',
u'天津市和平区二十中附小': u'70',
u'天津二街小学': u'71',
u'天津中心东道小学': u'72',
u'天津袁罗庄高级小学': u'73',
u'天津柳滩小学': u'74',
u'天津窦庄子联校': u'75',
u'天津蓟县上仓镇中心小学': u'76',
u'天津宝坻区大唐庄镇大唐庄中心小学': u'77',
u'天津白古屯乡小韩村完全小学': u'78',
u'天津北肖楼中心小学': u'79',
u'天津桥头小学': u'80',
u'天津岳会中心小学': u'81',
u'天津馨桥园小学': u'82',
u'天津劝业场小学': u'83',
u'天津西中心小学': u'84',
u'天津东海小学': u'85',
u'天津静海县大邱庄镇庞家庄中心小学': u'86',
u'天津西站小学': u'87',
u'天津第五中心小学': u'88',
u'天津大黄庄中心小学': u'89',
u'天津宁园小学': u'90',
u'天津同兴小学': u'91',
u'天津师范附属小学': u'92',
u'天津北塘一小': u'93',
u'天津下庄中心小学': u'94',
u'天津镇菱角沽中心小学': u'95',
u'天津希望小学': u'96',
u'天津市武清区崔黄口镇崔黄口中心小学': u'97',
u'天津蓟县侯家营镇侯家营中心小学': u'98',
u'天津是三街小学': u'99',
}
jn_dict = {
u'中国重型汽车集团公司济南第一小学': u'1',
u'济南市师范路小学': u'2',
u'济南市育明小学': u'3',
u'济南市历城区实验小学': u'4',
u'历城区王舍人镇实验小学': u'5',
u'济南市解放路第二小学': u'6',
u'济南青龙街小学': u'7',
u'济南市县西巷小学': u'8',
u'济南市北关小学': u'9',
u'济南美里湖第一小学': u'10',
u'济南市北大槐树第二小学': u'11',
u'济南市燕柳小学': u'12',
u'济南市天桥区黄台小学': u'13',
u'济南大正中心小学': u'14',
u'济南市甸柳第一小学(甸柳一小)': u'15',
u' 山东师大附小齐鲁合作学校': u'16',
u'济南市南上山街小学': u'17',
u'济南趵突泉路小学': u'18',
u'济南市纬三路小学': u'19',
u'济南第二十七中学': u'20',
u'济南市匡山小学': u'21',
u'济南市历城区洪家楼小学': u'22',
}
sjz_dict = {
u'石家庄市裕东小学': u'1',
u'石家庄市玉村小学': u'2',
u'石家庄市第六中学': u'3',
u'石家庄市八一小学': u'4',
u'晋州市和平路小学': u'5',
u'石家庄维明路小学': u'6',
u'石家庄外国语小学': u'7',
u'石家庄桥西区外国语小学': u'8',
u'石家庄神兴小学': u'9',
u'石家庄市东风西路小学': u'10',
u'裕华区阳光园小学': u'11',
u'石家庄市新华区柏林南路小': u'12',
u'石家庄联盟路小学': u'13',
u'石家庄桥西区实验小学': u'14',
u'石家庄市石岗大街第二小学': u'15',
u'晋州市魏征路小学': u'16',
u'石家庄市红星小学': u'17',
u'晋州市实验小学': u'18',
u'石家庄市回民小学': u'19',
u'石家庄市沿西街小学': u'20',
u'石家庄市麒麟私立中学': u'21',
u'四十三中小学': u'22',
u'白佛小学': u'23',
u'裕华区尖岭小学': u'24',
u'石家庄市西苑小学': u'25',
u'石家庄市华兴小学': u'26',
u'石家庄桥西区东里村小学': u'27',
u'石家庄兴华小学': u'28',
u'红鹰小学': u'29',
u'光明路小学': u'30',
u'石家庄市新华路小学': u'31',
u'石家庄市新华区党家庄学校': u'32',
u'石家庄市棉一小学': u'33',
u'石家庄桥西实验小学': u'34',
u'草场街小学': u'35',
u'石家庄育英小学': u'36',
u'石家庄桥西区第二外国语小': u'37',
u'裕华区东明小学': u'38',
u'石家庄市东苑小学': u'39',
u'石家庄和平西路小学': u'40',
u'石家庄友谊小学': u'41',
u'石家庄市跃进路小学': u'42',
u'石家庄市华英双语学校': u'43',
u'石家庄市宁安路小学': u'44',
u'石家庄中山路小学': u'45',
u'石家庄市跃进路小学': u'46',
u'石家庄草场街小学': u'47',
u'石家庄裕华西路小学': u'48',
u'石家庄市中华大街小学': u'49',
u'石家庄东苑小学': u'50',
}
mapper_dict = {'1': '一',
               '0': '零',
               '2': '二',
               '3': '三',
               '4': '四',
               '5': '五',
               '6': '六',
               '7': '七',
               '8': '八',
               '9': '九',
               # '10':'十'
               }

filter_dict = {}
def mapper_fun(val):
    if val.isdigit() and val in mapper_dict:
        return mapper_dict[val]
    return val


import traceback

update_db = DB()
from fuzzywuzzy import fuzz

where = '`city` = %s' % db.placeholder
update_where = '`name` = %s' % db.placeholder
for each in db._select2dic(where=where, what=['name','id'], where_values=(u'杭州',)):
    try:
        name = each['name']
        _id = each['id']
        name_deal = ''.join(map(mapper_fun, name.replace('杭州市', '').replace('杭州', '').replace('小学', '').replace('学校', '').replace('校区', '')))
        if filter_dict.has_key(name_deal):
            filter_dict[name_deal][1] += 1
        else:
            filter_dict[name_deal] = {'real_info':[{'name':name,'id': _id}],'repeat_times':[]}
    except:
        traceback.print_exc()
        continue

for k, v in filter_dict.iteritems():
    if v[1] !=0:
        print k, v[0],v[1]