# -*- coding: utf-8 -*-
import tsa_class

num = 1
num2 =1
#for i in range(10):
#    print(num)
#    num =num +num2
#    print (num2)
#    num2 = num + num2
tsa0=tsa_class.Temperature_Furnace(0.1)
#print(tsa0.t_furnace(0.2/60))
tsa1 = tsa_class.Surface_Fireporoofing(0.1)
tsa2 = tsa_class.Fp_to_Fp(0.1)
#print(tsa1.surface_FP(293,293,0.045645,0.011094055))
#print(tsa2.fp_to_fp(0,293.070051,293,293))
#print(tsa1.temp_surf)

temp_Tn = [20+273] * 9
#print(temp_Tn)
#print(temp_Tn[3])
temp_Tn0 =['A','B','C','D','E' ]
for A,_ in enumerate(temp_Tn0):
 if A == 0 : continue
 print(A,temp_Tn0[A])

classes = []
classes.append(tsa_class.Test_tsa(1, 'テスト１'))
classes.append(tsa_class.Test_tsa(2, 'テスト２'))

for test_cls in classes:
    print('===== Class =====')
    print('code --> ' + str(test_cls.code))
    print('name --> ' + test_cls.name)
  
