#ecoding:utf-8
import copy

al = [[1], [2], [3]]
bl = copy.copy(al)
cl = copy.deepcopy(al)

print "before=>"
print al
print bl
print cl

al[0][0] = 0
al[1] = None
al[2][0] = None

print "after=>"
print al
print bl
print cl

