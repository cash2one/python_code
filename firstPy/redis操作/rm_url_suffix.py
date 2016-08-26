import re
s= 'http://www.sd/i-sad/a/1'
print re.match(r'.*i-[^//]+',s).group()
print re.match(r'.*i-[^/]+',s).group()