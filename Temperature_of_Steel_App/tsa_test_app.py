# -*- coding: utf-8 -*-
import tsa_class

num = 1
num2 =1
#for i in range(10):
#    print(num)
#    num =num +num2
#    print (num2)
#    num2 = num + num2

#tsa_class1 = tsa_class.Temperature_calculation(0,1)
#tsa_class2 = tsa_class.Fp_to_Fp(3,1)
#tsa_class2.fp_to_fp()
#print(tsa_class2.time)
#tsa_class3 = tsa_class.Temperature_Furnace(4000,1)
#tsa_class3.t_furnace()
#print(tsa_class3.temp_F)
tsa_class4 = tsa_class.Surface_Heat_Transfer(0)
tsa_class5 = tsa_class.Temperature_Furnace(0)
tsa_class5.t_furnace(20)
print(tsa_class5.temp_F)
tsa_class4.surface_HT(tsa_class5.temp_F,1023.306236)
print(tsa_class4.qc,tsa_class4.qr)
if tsa_class4.qr < 10 :
    print('yes')

classes = []
classes.append(tsa_class.Test_tsa(1, 'テスト１'))
classes.append(tsa_class.Test_tsa(2, 'テスト２'))

for test_cls in classes:
    print('===== Class =====')
    print('code --> ' + str(test_cls.code))
    print('name --> ' + test_cls.name)
  
