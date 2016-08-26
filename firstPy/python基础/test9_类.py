# -*- coding: UTF-8 -*-
class Employee:
    '所有员工的基类'
    empCount = 0
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1
    def displayCount(self):
        print "Total Employee %d" % Employee.empCount

    def displayEmployee(self):
        print "Name:",self.name," Salary:", self.salary

emp1 = Employee("zhangsan",2000)
emp2 = Employee("lisi",3500)
emp1.displayCount()
emp1.displayEmployee()
print Employee.empCount
emp1.name = "zhangsan1"
emp1.age = 20;
emp1.displayEmployee()
print emp1.age
#del emp1.age
print hasattr(emp1,'age')
print hasattr(emp2,'age')
print getattr(emp2,'name')
setattr(emp2,'name','lisi1')
print getattr(emp2,'name')

print Employee.__name__
print Employee.__module__
print Employee.__doc__
print Employee.__dict__
print Employee.__bases__