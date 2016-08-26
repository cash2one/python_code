#ecoding:utf-8
import re
html_remove = re.compile(r'<[^>]+>',re.S)
print html_remove.match('<title>adaksd</title>').group()
#表示匹配字段用''替换,其实就是删除匹配字段!!!!!
print html_remove.sub('','<title>adaksd</title>')

date = '  2013-2-3 13:12'
date = re.findall('[0-9]+-[0-9]+-[0-9]+',date)
print date

#re.S表示多行匹配
text_split = re.compile(r'[0-9]+$',re.S)
print text_split.sub('','黄瓜中学12')
print text_split.search('黄瓜中学12').group()
print re.sub(r'[^0-9]+','','黄瓜中学12')
