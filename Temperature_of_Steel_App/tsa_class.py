# -*- coding: utf-8 -*-
import math
import configparser
from decimal import *

class Test_tsa:

 def __init__(self, code,name):
        self.code = code
        self.name = name


class Temperature_calculation:

    def __init__(self):
       inifile = configparser.ConfigParser()
       inifile.read('./tsa_config.ini', 'UTF-8') 
       self.data_save_path = inifile.get('settings', 'data_save_path')
       if inifile.get('settings', 'display_Kelvin') == "True" : self.disp_K = True
       elif inifile.get('settings', 'display_Kelvin') == "False" : self.disp_K = False
       else : print('settings,display_Kelvin Eror')
       self.d_time = Decimal  (inifile.get('settings', 'delta_time'))
       self.test_t = int (inifile.get('settings', 'testing_tiem'))
       self.temp_DF = float  (inifile.get('default-temperature', 'temperature_of_Furnace'))+273
       self.temp_F = self.temp_DF
       self.temp_FP = Decimal (inifile.get('default-temperature', 'temperature_of_Fireproofing'))+273
       self.temp_Steel = Decimal (inifile.get('default-temperature', 'temperature_of_Steel'))+273
       self.pf_sh = Decimal  (inifile.get('variable', 'specific_heat_of_Fireproofing'))
       self.pf_density = Decimal  (inifile.get('variable', 'density_of_Fireproofing'))
       self.steel_density = Decimal  (inifile.get('variable', 'density_of_Steel'))

    def pf_ther_conductivity(self,temp):
        conductivity_pf = 0
        if temp < 400 : conductivity_pf = Decimal( 0.09 )
        elif temp >= 400 and temp < 800 : conductivity_pf = Decimal((Decimal(0.11/400) * temp) -Decimal( 0.02) )
        elif temp >= 800 : conductivity_pf = Decimal((Decimal(0.09 / 200) * Decimal(temp)) - Decimal(0.16 )  )
        else : print('pf conductivity error')    
        return conductivity_pf

    def temperature_furnace(self,times):
        self.time=times
        self.temp_F =345* math.log10(8*self.time+1)+self.temp_DF
        return self.temp_F


class Surface_Fireporoofing(Temperature_calculation):

    def surface_Heat_Transfer(self,temp_f,temp_surf):
        temp_f = Decimal(temp_f)
        self.heat_flux_convection = Decimal  (Decimal(0.023)*(temp_f - temp_surf))
        self.heat_flux_radiation= Decimal(Decimal(5.67)*Decimal(10**-11)*Decimal(0.97)*((temp_f**4) - (temp_surf**4)))

    def surface_FP(self,temp_f,temp_surf,temp_T0):
        self.temp_T0 = temp_T0
        ther_conductivity = Decimal  (super().pf_ther_conductivity(temp_surf))
        self.surface_Heat_Transfer(temp_f,temp_surf)
        d_surf = Decimal  (0.625)
        d_tn =Decimal  (1.25 )
        len_x_surf =Decimal  (175-1.25)
        len_y_surf = Decimal  (225- 1.25)
        len_around_FP = Decimal( (225 + 175) * 2 * (10**-3) )
        len_around_surf = Decimal  ((len_x_surf + len_y_surf) * 2 * Decimal  (10**-3))
        area_surf = Decimal  (((175 * 225) - (len_x_surf * len_y_surf)) * Decimal  (10 ** -6))
        ther_resistivity_surf = Decimal  (self.d_time / (self.pf_density * self.pf_sh * area_surf) )
        power_per_len_convection = Decimal  ( len_around_FP *  self.heat_flux_convection )
        power_per_len_radiation = Decimal  (len_around_FP * self.heat_flux_radiation)
        power_per_len_conduction = Decimal ( len_around_surf * (ther_conductivity /(d_surf + (d_tn/2))) * ( temp_T0- temp_surf) )

        temp_surf = Decimal  (temp_surf + ther_resistivity_surf * (power_per_len_convection + power_per_len_radiation +power_per_len_conduction))

        return temp_surf


class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self,number_layer,temp_Tprev,temp_Tn,temp_Tnext):

        d_tn = Decimal  (1.25)
        len_x_Tprev = Decimal  (175 - (1.25 +2.5*(number_layer)))
        len_y_Tprev = Decimal  (225 - (1.25 +2.5*(number_layer)))
        len_x_Tn = Decimal  (175 - (1.25 +2.5*(number_layer+1)))
        len_y_Tn = Decimal  (225 - (1.25 +2.5*(number_layer+1)))
        len_around_Tprev = Decimal  ((len_x_Tprev + len_y_Tprev) * 2 * Decimal  (10 ** -3))
        len_around_Tnext = Decimal  ((len_x_Tn + len_y_Tn) * 2 * Decimal  (10 ** -3))
        area_Tn =Decimal  (((len_x_Tprev * len_y_Tprev) - (len_x_Tn * len_y_Tn) ) * Decimal  (10 ** -6))
        ther_conductivity = Decimal  (super().pf_ther_conductivity(temp_Tn))
        ther_resistivity_Tn = Decimal  (self.d_time / (self.pf_density * self.pf_sh * area_Tn))
        power_per_len_conduction_prev = Decimal  (len_around_Tprev * (ther_conductivity /((d_tn/2) + (d_tn/2)) ) * ( Decimal(temp_Tprev- temp_Tn)))
        power_per_len_conduction_next = Decimal  (len_around_Tnext * (ther_conductivity /((d_tn/2) + (d_tn/2)) ) * ( Decimal(temp_Tnext- temp_Tn)))
        
        temp_Tn = Decimal  (Decimal(temp_Tn) + ther_resistivity_Tn * (power_per_len_conduction_prev + power_per_len_conduction_next))

        return temp_Tn


class Fp_terminal(Temperature_calculation):

    def __steel_specific_heat (self,temp_steel):
        steel_sh = Decimal(Decimal(0.482) + 8 * Decimal(10 ** -10) * ((temp_steel - 273)**2))
        return steel_sh

    def fp_terminal(self,temp_Term_prev,temp_Term):
        self.temp_Term = Decimal  (temp_Term)
        steel_sh = Decimal  (self.__steel_specific_heat(temp_Term))
        d_tn = Decimal  (1.25)
        d_Term = Decimal  (0.625)
        len_x_Term_prev = Decimal  (175 - (1.25 +2.5*9 ))
        len_y_Term_prev = Decimal  (225 - (1.25 +2.5*9 ))
        len_x_Term = Decimal  (175 - (1.25 +2.5*9 + 1.25))
        len_y_Term = Decimal  (225 - (1.25 +2.5*9 + 1.25))
        len_around_Term_prev = Decimal  ((len_x_Term_prev + len_y_Term_prev) * 2 * Decimal  (10 ** -3))
        area_Term = Decimal  (((len_x_Term_prev * len_y_Term_prev) - (len_x_Term * len_y_Term) ) * Decimal  (10 ** -6))
        area_S = Decimal  (0.005976)
        ther_conductivity_Term =Decimal  ( super().pf_ther_conductivity(self.temp_Term))
        ther_resistivity_Term = Decimal  (self.d_time / ((self.pf_density * self.pf_sh * area_Term) + (self.steel_density * steel_sh * area_S)))

        self.temp_Term = Decimal  (temp_Term + ther_resistivity_Term * (   len_around_Term_prev * ther_conductivity_Term / ((d_tn / 2)+ d_Term)  )*(temp_Term_prev - temp_Term))

        return self.temp_Term
