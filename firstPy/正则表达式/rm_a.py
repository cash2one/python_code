#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
import re
reload(sys)
sys.setdefaultencoding("utf-8")
pattern = re.compile(r'<a.*?">',re.S)
def removeLink(content):
    contents = ''
    for link in pattern.findall(content):
        content = content.replace(link,'')
    contents += content
    return  contents

ss = '''下载手机一、单项选择题(本类题共10小题，每小题1分。共10分。每小题备选答案中。只有一个符合题意的正确答案，多选、错选、不选均不得分)<br />1．下列选项中，对通用会计软件的说法不正确的是（　　）。 <br />A．由软件公司负责维护 <br />B．能满足企业的大部分需求 <br />C．软件安全保密性强 <br />D．为本单位使用而开发 <br />2．下列叙述正确的是（　　）。 <br />A．会计电算化是会计信息化的初级阶段和基础工作 <br />B．实施会计电算化为的是增加会计人员就业 <br />C．实施会计电算化为的是提高计算机技术水平 <br />D．实施会计电算化为的是提高会计人员待遇 <br />3．会计软件属于（　　）。 <br />A．文字处理软件 <br />B．应用软件 <br />C．支持性软件 <br />D．操作软件 <br />4．广域网的覆盖范围最大可以是（　　）。 <br />A．多个国家 <br />B．整个世界 <br />C．整个城市 <br />D．一个国家 <br />5．下列各项中，不属于非规范化操作的是（　　）。 <br />A．未按照正常操作规范运行软件 <br />B．期末未按时结账 <br />C．密码与权限管理不当 <br />D．会计档案保存不当 <br />6．下列选项中，不能做到“只关闭当前文件，其他处于打开状态的Excel文件仍处于打开状态”的操作方法是（　　）。 <br />A．按击快捷键“Ctrl+F4”<br />B．点击菜单栏最右边的关闭按钮“×”<br />C．点击标题栏最右边的关闭按钮“X”<br />D．点击“文件”下拉菜单的“关闭”按钮 <br />7．当企业涉及外币业务时，应进行的设置是（　　）。 <br />A．收付结算 <br />B．外币设置 <br />C．会计科目 <br />D．凭证类别 <br />8．下列各项中，不属于工资管理模块期末处理的是（　　）。 <br />A．工资分摊 <br />B．工资表输出 <br />C．工资表查询 <br />D．期末结账 <br />9．计算机黑客在进行密码破解时常用的手段是（　　）。 <br />A．字典攻击 <br />B．网络监听 <br />C．攻击系统漏洞 <br />D．端口扫描 <br />10．启动Excel 2003后建立的第一个空白工作簿的文件名是（　　）。 <br />A．Sheet1．xlsx<br />B．Boom．xlsx<br />C．Sheet1．xls <br />D．Book1．xls
<strong>编辑推荐：</strong><a href="http://www.233.com/cy/moniti/" target="_blank"><font color="#0000ff">天津会计从业资格考试试题</font></a> | <a href="http://www.233.com/cy/tiku/" target="_blank"><font color="#0000ff">天津会计从业资格考试题库</font></a>&#13;
&#13;'''
print removeLink(ss)
s = Tr