# -*- coding: utf-8 -*-
import math
class Test_tsa:

 def __init__(self, code,name):
        self.code = code
        self.name = name


class Temperature_calculation:

    def __init__(self,delta_time):
       self.d_time = delta_time
       self.ci = 1
       self.rho_i = 130
       self.cs = 0.482
       self.rho_s = 7850
       
     
       # super().__init__(num1, num2)
class Temperature_Furnace(Temperature_calculation):

    def t_furnace(self,times):
        self.time=times
        self.temp_F =345* math.log10(8*self.time+1)+20+273
        return self.temp_F

class Surface_Heat_Transfer(Temperature_calculation):

    #def __init__(self,qc,qr):
    #    self.qc=qc
    #    self.qr=qr
        
    def surface_HT(self,temp_F,temp_surf):
        self.temp_F = temp_F
        self.temp_surf = temp_surf
        self.qc = 0.023*(self.temp_F - self.temp_surf)
        self.qr = 5.67*(10**-11)*0.97*((self.temp_F**4) - (self.temp_surf**4))

class Surface_Fireporoofing(Temperature_calculation):
    
    def surface_FP(self,temp_surf,temp_T0,qc,qr):
        self.temp_surf = temp_surf
        ther_conductivity = 0.09
        d_surf = 0.625
        d_tn =1.25
        len_x_surf =175-1.25
        len_y_surf = 225- 1.25
        len_around_FP = (225 + 175) * 2 * (10**-3)
        len_around_surf = (len_x_surf + len_y_surf) * 2 * (10**-3)
        area_surf = ((175 * 225) - (len_x_surf * len_y_surf)) * (10 ** -6)
        ther_resistivity_surf = self.d_time / (self.rho_i * self.ci * area_surf)
        power_per_len_convection = len_around_FP * qc
        power_per_len_radiation = len_around_FP *qr
        power_per_len_conduction = len_around_surf * (ther_conductivity /(d_surf + (d_tn/2))) * ( temp_T0- temp_surf)
        self.temp_surf = temp_surf + ther_resistivity_surf * (power_per_len_convection + power_per_len_radiation +power_per_len_conduction)

        return self.temp_surf

class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self,number_sheaf,temp_Tprev,temp_Tn,temp_Tnext):
        self.temp_Tn = temp_Tn
        d_tn = 1.25
        len_x_Tprev = 175 - (1.25 +2.5*(number_sheaf))
        len_y_Tprev = 225 - (1.25 +2.5*(number_sheaf))
        len_x_Tn = 175 - (1.25 +2.5*(number_sheaf+1))
        len_y_Tn = 225 - (1.25 +2.5*(number_sheaf+1))
        len_around_Tprev = (len_x_Tprev + len_y_Tprev) * 2 * (10 ** -3)
        len_around_Tnext = (len_x_Tn + len_y_Tn) * 2 * (10 ** -3)
        area_Tn =((len_x_Tprev * len_y_Tprev) - (len_x_Tn * len_y_Tn) ) * (10 ** -6)
        ther_conductivity_prev = 0.09
        ther_conductivity_next = 0.09
        ther_resistivity_Tn = self.d_time / (self.rho_i * self.ci * area_Tn)
        power_per_len_conduction_prev = len_around_Tprev * (ther_conductivity_prev /((d_tn/2) + (d_tn/2)) ) * ( temp_Tprev- temp_Tn)
        power_per_len_conduction_next = len_around_Tnext * (ther_conductivity_next /((d_tn/2) + (d_tn/2)) ) * ( temp_Tnext- temp_Tn)
        self.temp_Tn = temp_Tn + ther_resistivity_Tn * (power_per_len_conduction_prev + power_per_len_conduction_next)
        
        #print(number_sheaf,temp_Tprev,temp_Tn,temp_Tnext)
        return self.temp_Tn

class Fp_terminal(Temperature_calculation):

    def fp_terminal(self,temp_Term_prev,temp_Term):
        self.temp_Term = temp_Term
        d_tn = 12.5
        d_Term = 6.25
        len_x_Term_prev = 175 - (1.25 +2.5*9 )
        len_y_Term_prev = 225 - (1.25 +2.5*9 )
        len_x_Term = 175 - (1.25 +2.5*9 + 1.25)
        len_y_Term = 225 - (1.25 +2.5*9 + 1.25)
        len_around_Term_prev = (len_x_Term_prev + len_y_Term_prev) * 2 * (10 ** -3)
        area_Term = ((len_x_Term_prev * len_y_Term_prev) - (len_x_Term * len_y_Term) ) * (10 ** -6)
        area_S = 0.005976
        ther_conductivity_Term = 0.9
        ther_resistivity_Term = self.d_time / (self.rho_i * self.ci * area_Term + self.rho_s * self.cs * area_S)
        self.temp_Term = temp_Term + ther_resistivity_Term * ( len_around_Term_prev * ther_conductivity_Term / ((d_tn/2)+ d_Term))*(temp_Term_prev - temp_Term)

       # print(ther_resistivity_Term,len_around_Term_prev,ther_conductivity_Term)
        return self.temp_Term
 