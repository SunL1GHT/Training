# class Dog:
#     def __init__(self,name,age,breed,master):    # 实例属性
#         self.names = name
#         self.ages = age
#         self.breeds = breed
#         self.masters = master    # master传进来应为对象

#     def sayhi(self):
#         print('Hi, I\'m %s,a %s dog,my master is %s' % (self.names, self.breeds, self.masters.name))# 依赖关系

# class Person:
#     def __init__(self,name,age,sex):
#         self.name = name
#         self.age = age
#         self.sex = sex

#     def walk_dog(self,dog_obj):
#         print('主人[%s]带狗[%s]去溜溜。。。'%(self.name, dog_obj.name))

# p1 = Person('二郎神',108,'Male')
# d1 = Dog('哮天犬',2,'二哈',p1)

# # d1.sayhi()
# # p1.walk_dog(d1)

# print(d1.masters.name)

import cv2

img = cv2.imread("/home/gxg/Desktop/Training/CamCalib/Calibsource/calib2.jpg")
print(img)
cv2.imshow('img',img)
cv2.waitKey(0)