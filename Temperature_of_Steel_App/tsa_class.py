# -*- coding: utf-8 -*-
class Test_tsa:

 def __init__(self, code,name):
        self.code = code
        self.name = name



class Temperature_calculation:

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
       # super().__init__(num1, num2)


class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self):
        self.num1=self.num1+self.num2
 