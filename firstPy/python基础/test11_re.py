#-*- coding: utf-8 -*-
import  re
line = "Cats are smarter than dogs"
#字符串前面加r，表示的意思是禁止字符串转义
matchobj = re.match(r'(.*) are (.*?o)(.*)', line)
if matchobj:
    #有多少括号就有多少group
    print matchobj.group()
    print matchobj.group(1)
    print matchobj.group(2)
    print matchobj.group(3)
else:
    print "No match!"

str = 'tiku/asdj.html'
if re.match('tiku/(.*).html',str):
    print True
if 'tiku/' in str and '.html' in str:
    print  "ok"