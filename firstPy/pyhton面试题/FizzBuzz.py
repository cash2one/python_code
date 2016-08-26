#ecoding:utf8
#写一个程序，打印数字1到100，3的倍数打印“Fizz”来替换这个数，
# 5的倍数打印“Buzz”，对于既是3的倍数又是5的倍数的数字打印“FizzBuzz”。

for x in range(101):
    print "fizz"[x%3*4::]+"buzz"[x%5*4::]or x
