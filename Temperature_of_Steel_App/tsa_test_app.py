# -*- coding: utf-8 -*-
import tsa_class

num = 1
num2 =1
#for i in range(10):
#    print(num)
#    num =num +num2
#    print (num2)
#    num2 = num + num2

tsa_class1 = tsa_class.Temperature_calculation(0,1)
tsa_class2 = tsa_class.Fp_to_Fp(3,1)
tsa_class2.fp_to_fp()
print(tsa_class2.num1)

classes = []
classes.append(tsa_class.Test_tsa(1, 'テスト１'))
classes.append(tsa_class.Test_tsa(2, 'テスト２'))

for test_cls in classes:
    print('===== Class =====')
    print('code --> ' + str(test_cls.code))
    print('name --> ' + test_cls.name)
  
