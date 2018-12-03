# -*- coding: utf-8 -*-
import math
class Test_tsa:

 def __init__(self, code,name):
        self.code = code
        self.name = name


class Temperature_calculation:

    def __init__(self,time):
       self.time = time
     
       # super().__init__(num1, num2)
class Temperature_Furnace(Temperature_calculation):

    def t_furnace(self,times):
        self.time=times
        self.temp_F =345* math.log10(8*self.time+1)+20+273

class Surface_Heat_Transfer(Temperature_calculation):

    #def __init__(self,qc,qr):
    #    self.qc=qc
    #    self.qr=qr
        
    def surface_HT(self,temp_F,temp_surf):
        self.qc=0.023*(temp_F-temp_surf)
        self.qr=5.67*(10**-11)*0.97*((temp_F**4)-(temp_surf**4)

class Surface_Fireporoofing(Temperature_calculation):

    def surface_FP():
        A = 0

class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self):
          A = 0
 