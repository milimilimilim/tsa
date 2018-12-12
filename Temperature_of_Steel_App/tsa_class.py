# -*- coding: utf-8 -*-
import math
import configparser
from decimal import *

class Test_tsa:

 def __init__(self, code,name):
        self.code = code
        self.name = name

class Loading_input_value :

    def __init__(self):
        pass

    def loading_ini (self) :
        inifile = configparser.ConfigParser()
        inifile.read('./tsa_config.ini', 'UTF-8') 
        self.data_save_path = inifile.get('settings', 'data_save_path')
        if inifile.get('settings', 'display_Kelvin') == "True" : self.disp_K = True
        elif inifile.get('settings', 'display_Kelvin') == "False" : self.disp_K = False
        else : print('settings,display_Kelvin Eror')
        self.d_time = Decimal  (inifile.get('settings', 'delta_time'))
        self.width_steel = Decimal  (inifile.get('Test_Specimens','width_of_steel'))* Decimal (10**-3)
        self.heigth_steel =Decimal  (inifile.get('Test_Specimens','heigth_of_steel'))* Decimal (10**-3)
        self.thickness_FP = Decimal  (inifile.get('Test_Specimens','thickness_of_Fireproofing'))* Decimal (10**-3)
        self.total_layer = int( inifile.get('Test_Specimens', 'number_of_layer') )
        self.len_surf = Decimal  (inifile.get('Test_Specimens', 'thickness_of_FP_surface'))* Decimal (10**-3)
        self.len_Term = Decimal  ( inifile.get('Test_Specimens', 'thickness_of_FP_surface'))* Decimal (10**-3)
        self.width_TP = self.width_steel + (self.thickness_FP * 2)
        self.heigth_TP = self.heigth_steel + (self.thickness_FP * 2)
        self.len_Tn = (self.thickness_FP - self.len_surf -  self.len_Term)/self.total_layer
        self.test_t = int (inifile.get('settings', 'testing_time'))
        self.temp_DF = float  (inifile.get('default-temperature', 'temperature_of_Furnace'))+273
        self.temp_F = self.temp_DF
        self.temp_FP = Decimal (inifile.get('default-temperature', 'temperature_of_Fireproofing'))+273
        self.temp_Steel = Decimal (inifile.get('default-temperature', 'temperature_of_Steel'))+273
        self.pf_sh = Decimal  (inifile.get('variable', 'specific_heat_of_Fireproofing'))
        self.pf_density = Decimal  (inifile.get('variable', 'density_of_Fireproofing'))
        self.steel_density = Decimal  (inifile.get('variable', 'density_of_Steel'))

       


class Temperature_calculation:

    def __init__(self,ini_input):

       self.d_time = ini_input.d_time
       self.width_steel = ini_input.width_steel
       self.heigth_steel =ini_input.heigth_steel
       self.thickness_FP = ini_input.thickness_FP 
       self.total_layer = ini_input.total_layer
       self.len_surf = ini_input.len_surf
       self.len_Term =  ini_input.len_Term
       self.width_TP = ini_input.width_TP
       self.heigth_TP = ini_input.heigth_TP
       self.len_Tn = ini_input.len_Tn
       self.test_t = ini_input.test_t
       self.temp_DF = ini_input.temp_DF
       self.temp_F = ini_input.temp_F
       self.temp_FP = ini_input.temp_FP
       self.temp_Steel = ini_input.temp_Steel
       self.pf_sh = ini_input.pf_sh
       self.pf_density = ini_input.pf_density
       self.steel_density = ini_input.steel_density

       
     
    def pf_ther_conductivity(self,temp):
        conductivity_pf = 0
        if temp < 400 : conductivity_pf = Decimal( 0.09 )
        elif temp >= 400 and temp < 800 : conductivity_pf = Decimal((Decimal(0.11/400) * temp) -Decimal( 0.02) )
        elif temp >= 800 : conductivity_pf = Decimal((Decimal(0.09 / 200) * Decimal(temp)) - Decimal(0.16 )  )
        else : print('pf conductivity error')    
        return conductivity_pf

    def temperature_furnace(self,times):
        temp_F =345* math.log10(8*times+1)+self.temp_DF
        return temp_F

    def cal_tempMax(self):
        temp_max = self.temperature_furnace(self.test_t)
        self.tempMAX = (temp_max // 100 )*100 + 100
        return self.tempMAX
      

class Stability_Analysis (Temperature_calculation):

    def cal_stability_time (self,cal_temp):
        len_min = self.cal_min_len(self.len_Tn,self.cal_min_len(cal_temp.len_surf,cal_temp.len_Term))
        print(len_min)
        stability_time =Decimal (Decimal (cal_temp.pf_sh * cal_temp.pf_density * Decimal (len_min ** 2)) / Decimal(2 * self.pf_ther_conductivity(cal_temp.tempMAX)))
        E_10 =int ( 0 )
        while (stability_time//1 == 0) :
            stability_time=stability_time*10
            E_10 = E_10 +1
        print(stability_time,E_10)
        stability_time= Decimal(stability_time//Decimal(0.1))/10
        self.stability_time = Decimal( stability_time ) * Decimal(10**(-1*E_10))

        return self.stability_time
    def cal_total_time (self,cal_temp):
        total_test_time = ( (cal_temp.test_t*60/cal_temp.d_time)*Decimal(0.00002)*cal_temp.total_layer) / 3600
        return total_test_time
    def cal_min_len(self,A,B):
        if A<= B : return A
        else: return B

    def tiems () :
        pass


class Surface_Fireporoofing(Temperature_calculation):

    def surface_Heat_Transfer(self,temp_f,temp_surf):
        temp_f = Decimal(temp_f)
        self.heat_flux_convection = Decimal  (Decimal(0.023)*(temp_f - temp_surf))
        self.heat_flux_radiation= float((5.67)*(10**-11)*(0.97)*(float(temp_f**4) - float(temp_surf**4)))

    def surface_FP(self,temp_f,temp_surf,temp_T0):
        self.temp_T0 = temp_T0
        ther_conductivity = Decimal  (super().pf_ther_conductivity(temp_surf))
        self.surface_Heat_Transfer(temp_f,temp_surf)
        len_x_surf = Decimal  (self.width_TP - self.len_surf)
        len_y_surf = Decimal  (self.heigth_TP - self.len_surf)
        len_around_FP = Decimal( (self.heigth_TP + self.width_TP) * 2 )
        len_around_surf = Decimal  ((len_x_surf + len_y_surf) * 2 )
        area_surf = Decimal  (((self.width_TP * self.heigth_TP) - (len_x_surf * len_y_surf)) )
        ther_resistivity_surf = Decimal  (self.d_time / (self.pf_density * self.pf_sh * area_surf) )
        power_per_len_convection = Decimal  ( len_around_FP *  self.heat_flux_convection )
        power_per_len_radiation = Decimal  (len_around_FP * Decimal(self.heat_flux_radiation))
        power_per_len_conduction = Decimal ( len_around_surf * (ther_conductivity /(self.len_surf + (self.len_Tn/2))) * ( temp_T0- temp_surf) )

        temp_surf = Decimal  (temp_surf + ther_resistivity_surf * (power_per_len_convection + power_per_len_radiation +power_per_len_conduction))

        return temp_surf


class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self,number_layer,temp_Tprev,temp_Tn,temp_Tnext):

        len_x_Tprev = Decimal  (self.width_TP  - (self.len_surf +self.len_Tn*number_layer))
        len_y_Tprev = Decimal  (self.heigth_TP - (self.len_surf +self.len_Tn*number_layer))
        len_x_Tn = Decimal  (self.width_TP  - (self.len_surf +self.len_Tn*(number_layer+1)))
        len_y_Tn = Decimal  (self.heigth_TP - (self.len_surf +self.len_Tn*(number_layer+1)))
        len_around_Tprev = Decimal  ((len_x_Tprev + len_y_Tprev) * 2 )
        len_around_Tnext = Decimal  ((len_x_Tn + len_y_Tn) * 2 )
        area_Tn =Decimal  ((len_x_Tprev * len_y_Tprev) - (len_x_Tn * len_y_Tn) )
        ther_conductivity = Decimal  (super().pf_ther_conductivity(temp_Tn))
        ther_resistivity_Tn = Decimal  (self.d_time / (self.pf_density * self.pf_sh * area_Tn))
        power_per_len_conduction_prev = Decimal  (len_around_Tprev * (ther_conductivity /((self.len_Tn/2) + (self.len_Tn/2)) ) * ( Decimal(temp_Tprev- temp_Tn)))
        power_per_len_conduction_next = Decimal  (len_around_Tnext * (ther_conductivity /((self.len_Tn/2) + (self.len_Tn/2)) ) * ( Decimal(temp_Tnext- temp_Tn)))
        
        temp_Tn = Decimal  (Decimal(temp_Tn) + ther_resistivity_Tn * (power_per_len_conduction_prev + power_per_len_conduction_next))

        return temp_Tn


class Fp_terminal(Temperature_calculation):

    def __steel_specific_heat (self,temp_steel):
        steel_sh = Decimal(Decimal(0.482) + 8 * Decimal(10 ** -10) * ((temp_steel - 273)**2))
        return steel_sh

    def fp_terminal(self,temp_Term_prev,temp_Term):
        self.temp_Term = Decimal  (temp_Term)
        steel_sh = Decimal  (self.__steel_specific_heat(temp_Term))
        len_x_Term_prev = Decimal  (self.width_TP  - (self.len_surf +self.len_Tn*self.total_layer))
        len_y_Term_prev = Decimal  (self.heigth_TP - (self.len_surf +self.len_Tn*self.total_layer))
        len_x_Term = Decimal  (self.width_TP  - (self.len_surf +self.len_Tn*self.total_layer+self.len_Term))
        len_y_Term = Decimal  (self.heigth_TP - (self.len_surf +self.len_Tn*self.total_layer+self.len_Term))
        len_around_Term_prev = Decimal  ((len_x_Term_prev + len_y_Term_prev) * 2 )
        area_Term = Decimal  (((len_x_Term_prev * len_y_Term_prev) - (len_x_Term * len_y_Term) ) )
        area_S = Decimal  (0.005976)
        ther_conductivity_Term =Decimal  ( super().pf_ther_conductivity(self.temp_Term))
        ther_resistivity_Term = Decimal  (self.d_time / ((self.pf_density * self.pf_sh * area_Term) + (self.steel_density * steel_sh * area_S)))

        self.temp_Term = Decimal  (temp_Term + ther_resistivity_Term * (   len_around_Term_prev * ther_conductivity_Term / ((self.len_Tn / 2)+ self.len_Term)  )*(temp_Term_prev - temp_Term))

        return self.temp_Term
