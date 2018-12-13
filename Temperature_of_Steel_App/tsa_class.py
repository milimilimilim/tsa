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

        #save path
        self.data_save_path = inifile.get('settings', 'data_save_path')

        #test detail
        self.d_time = Decimal  (inifile.get('settings', 'delta_time'))
        self.disp_K = bool (self.true_or_false ('settings , display_Kelvin',inifile.get('settings', 'display_Kelvin')))
        self.test_t = int (inifile.get('settings', 'testing_time'))
        self.u_floor = bool (self.true_or_false ('Test_Specimens , under_floor',inifile.get('Test_Specimens', 'under_floor')))

        #test specimen
        self.type_Steel = inifile.get('Test_Specimens', 'type_of_steel')
        self.type_FP = inifile.get('Test_Specimens', 'type_of_Firepoofing')
        #test specimen detail
        self.width_steel = Decimal  (inifile.get('Test_Specimens','width_of_steel'))* Decimal (10**-3)
        self.heigth_steel =Decimal  (inifile.get('Test_Specimens','heigth_of_steel'))* Decimal (10**-3)
        self.thickness_Steel = Decimal  (inifile.get('Test_Specimens','thickness_of_steel'))* Decimal (10**-3)
        self.thickness_Steel_web = Decimal  (inifile.get('Test_Specimens','thickness_of_steel_web'))* Decimal (10**-3)
        self.thickness_Steel_flang = Decimal  (inifile.get('Test_Specimens','thickness_of_steel_flang'))* Decimal (10**-3)
        self.thickness_FP = Decimal  (inifile.get('Test_Specimens','thickness_of_Fireproofing'))* Decimal (10**-3)

        self.width_TP = self.width_steel + (self.thickness_FP * 2)
        self.heigth_TP = self.heigth_steel + (self.thickness_FP * 2)
        self.width_inside_steel = self.width_steel - (2 * self.thickness_Steel)
        self.heigth_inside_steel = self.heigth_steel - (2 * self.thickness_Steel)
        #layer detail
        self.total_layer = int( inifile.get('Test_Specimens', 'number_of_layer') )
        self.len_surf = Decimal  (inifile.get('Test_Specimens', 'thickness_of_FP_surface'))* Decimal (10**-3)
        self.len_Term = Decimal  ( inifile.get('Test_Specimens', 'thickness_of_FP_surface'))* Decimal (10**-3)
        self.len_Tn = (self.thickness_FP - self.len_surf -  self.len_Term)/self.total_layer

        #Default temperature
        self.temp_DF = float  (inifile.get('default-temperature', 'temperature_of_Furnace'))+273
        self.temp_F = self.temp_DF
        self.temp_FP = Decimal (inifile.get('default-temperature', 'temperature_of_Fireproofing'))+273
        self.temp_Steel = Decimal (inifile.get('default-temperature', 'temperature_of_Steel'))+273

        #elements value
        self.emissivity_pf = float  (inifile.get('variable', 'emissivity_of_Fireproofing'))
        self.pf_sh = Decimal  (inifile.get('variable', 'specific_heat_of_Fireproofing'))
        self.pf_density = Decimal  (inifile.get('variable', 'density_of_Fireproofing'))
        self.steel_density = Decimal  (inifile.get('variable', 'density_of_Steel'))

    def true_or_false (self,jd_name,judg):
        if judg == "True" : return True
        elif judg == "False" : return False
        else : print(jd_name+' Eror')

       


class Temperature_calculation:

    def __init__(self,ini_input):

       self.type_FP = ini_input.type_FP
       self.d_time = ini_input.d_time
       self.u_floor = ini_input.u_floor
       self.width_steel = ini_input.width_steel
       self.heigth_steel =ini_input.heigth_steel
       self.thickness_FP = ini_input.thickness_FP 
       self.total_layer = int (ini_input.total_layer)
       self.len_surf = ini_input.len_surf
       self.len_Term =  ini_input.len_Term
       self.width_TP = ini_input.width_TP
       self.heigth_TP = ini_input.heigth_TP
       self.width_inside_steel = ini_input.width_inside_steel
       self.heigth_inside_steel = ini_input.heigth_inside_steel
       self.len_Tn = ini_input.len_Tn
       self.test_t = ini_input.test_t
       self.temp_DF = ini_input.temp_DF
       self.temp_F = ini_input.temp_F
       self.temp_FP = ini_input.temp_FP
       self.temp_Steel = ini_input.temp_Steel
       self.pf_sh = ini_input.pf_sh
       self.pf_density = ini_input.pf_density
       self.steel_density = ini_input.steel_density
       self.emissivity_pf = ini_input.emissivity_pf
       self.type_Steel = ini_input.type_Steel
       self.thickness_Steel = ini_input.thickness_Steel
       self.thickness_Steel_web = ini_input.thickness_Steel_web
       self.thickness_Steel_flang = ini_input.thickness_Steel_flang

       self.fp_thick = [0 for i in range(self.total_layer+3)]
       self.cal_Fp_thick()
       self.len_wh_TP = [[0 for i in range(2)] for j in range(self.total_layer+3)]
       self.cal_len_wh_TP()
       self.len_around = [0 for i in range(self.total_layer+3)]
       self.cal_len_around()
       self.area_TS = [0 for i in range(self.total_layer+3)]
       self.cal_area()
       if self.u_floor:
           self.len_around[0] = self.len_around[0] - self.len_wh_TP[0][0]


       for i in range (self.total_layer+3):
           print("thick=="+str(self.fp_thick[i])+"\n")
       for i in range (self.total_layer+3):
           print("array=="+str(self.len_wh_TP[i])+"\n")
       for i in range (self.total_layer+3):
           print("around=="+str(self.len_around[i])+"\n")
       for i in range (self.total_layer+3):
           print("area=="+str(self.area_TS[i])+"\n")
       
     
    def pf_ther_conductivity(self,temp):
        if self.type_FP == 'mineral_wool':
             conductivity_pf = 0
             self.temp_k = float(temp)
             conductivity_pf = Decimal(6.71*(10**-5))
        elif self.type_FP == 'ceramic_fiber' :
            conductivity_pf = 0
            if temp < 400 : conductivity_pf = Decimal( 0.00009 )
            elif temp >= 400 and temp < 800 : conductivity_pf = Decimal(Decimal((Decimal(0.11/400) * temp) -Decimal( 0.02) )*Decimal(10**-3))
            elif temp >= 800 : conductivity_pf =Decimal( Decimal((Decimal(0.09 / 200) * Decimal(temp)) - Decimal(0.16 )  )*Decimal(10**-3))
            else : print('pf conductivity error2')    
        else:print('pf conductivity error0')   
        return conductivity_pf

    def temperature_furnace(self,times):
        temp_F =345* math.log10(8*times+1)+self.temp_DF
        return temp_F

    def cal_tempMax(self):
        temp_max = self.temperature_furnace(self.test_t)
        self.tempMAX = (temp_max // 100 )*100 + 100
        return self.tempMAX

    def  cal_Fp_thick (self):
        for i in range (self.total_layer+3):
            if i == 0 : self.fp_thick[0] = self.thickness_FP
            elif i == self.total_layer+2 : self.fp_thick[self.total_layer+2] = 0
            else :self.fp_thick[i] = self.thickness_FP - (self.len_surf +self.len_Tn*(i - 1))


    def cal_len_wh_TP (self) :
       self.len_wh_TP[0][0]  = self.width_TP
       self.len_wh_TP[0][1] = self.heigth_TP
       self.len_wh_TP[1][0]  = self.cal_len_FP_width('surf')
       self.len_wh_TP[1][1] = self.cal_len_FP_heigth('surf')
       self.len_wh_TP[self.total_layer+2][0]  = self.cal_len_FP_width('term')
       self.len_wh_TP[self.total_layer+2][1] = self.cal_len_FP_heigth('term')
       for i in range(self.total_layer):
           self.len_wh_TP[i+2][0]  = self.cal_len_FP_width(i+1)
           self.len_wh_TP[i+2][1]  = self.cal_len_FP_heigth(i+1)

    def cal_len_FP_width (self,layer):
        len_fn = 0
        if layer == 'surf': namber_layer = 0
        elif layer == 'term' :
            namber_layer = self.total_layer
            len_fn = self.len_Term
        else : namber_layer = layer
        len_fp_width = Decimal  (self.width_TP  - 2 * (self.len_surf +self.len_Tn*namber_layer+len_fn))
        return len_fp_width

    def cal_len_FP_heigth (self,layer):
        len_fn = 0
        if layer == 'surf': namber_layer = 0
        elif layer == 'term'  :
            namber_layer = self.total_layer
            len_fn = self.len_Term
        else : namber_layer = layer
        len_fp_heigth = Decimal  (self.heigth_TP - 2 * (self.len_surf +self.len_Tn*namber_layer+len_fn))
        return len_fp_heigth

    def cal_len_around (self):
        if self.type_Steel == 'square' :
            for i in range(self.total_layer+3):
                self.len_around[i] =2 * (self.len_wh_TP[i][0]+self.len_wh_TP[i][1])
        elif self.type_Steel == 'H-beam' :
            for i in range(self.total_layer+3):
                self.len_around[i] =2 * (self.len_wh_TP[i][0]+self.len_wh_TP[i][1]) + (2 * (self.width_steel - self.thickness_Steel_web))

    def cal_area (self):
        if self.type_Steel == 'square' :
            for i in range(self.total_layer+2):
                self.area_TS[i] = self.len_wh_TP[i][0]* self.len_wh_TP[i][1] - self.len_wh_TP[i+1][0]* self.len_wh_TP[i+1][1]
            self.area_TS[self.total_layer+2] = (self.len_wh_TP[self.total_layer+2][0]*self.len_wh_TP[self.total_layer+2][1]) - (self.width_inside_steel * self.heigth_inside_steel)
        elif self.type_Steel == 'H-beam' :
            for i in range(self.total_layer+2):
                self.area_TS[i] = self.cal_H_area(i) - self.cal_H_area(i+1)
            self.area_TS[self.total_layer+2] = (2*(self.width_steel*self.thickness_Steel_flang) + ((self.heigth_steel - (2 * self.thickness_Steel_flang)) *self.thickness_Steel_web))

    def cal_H_area(self,n_layer):
        h_area = ( self.len_wh_TP[n_layer][0]* self.len_wh_TP[n_layer][1] )-  ((self.heigth_steel- (2*(self.fp_thick[n_layer]+self.thickness_Steel_flang))) * (self.width_steel - self.thickness_Steel_web))

        return h_area

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
        self.heat_flux_radiation= float((5.67)*(10**-11)*(self.emissivity_pf)*(float(temp_f**4) - float(temp_surf**4)))

    def surface_FP(self,temp_f,temp_surf,temp_T0):
        self.temp_T0 = temp_T0
        ther_conductivity = Decimal  (super().pf_ther_conductivity(temp_surf))
        self.surface_Heat_Transfer(temp_f,temp_surf)

        len_x_surf =  self.len_wh_TP[1][0]
        len_y_surf =  self.len_wh_TP[1][1]


        len_around_FP = Decimal( self.len_around[0] )
        len_around_inside_surf = Decimal  (self.len_around[1])

        area_surf = Decimal  (self.area_TS[0])

        ther_resistivity_surf = Decimal  (self.d_time / (self.pf_density * self.pf_sh * area_surf) )
        power_per_len_convection = Decimal  ( len_around_FP *  self.heat_flux_convection )
        power_per_len_radiation = Decimal  (len_around_FP * Decimal(self.heat_flux_radiation))
        power_per_len_conduction = Decimal ( len_around_inside_surf * (ther_conductivity /(self.len_surf + (self.len_Tn/2))) * ( temp_T0- temp_surf) )

        temp_surf = Decimal  (temp_surf + ther_resistivity_surf * (power_per_len_convection + power_per_len_radiation +power_per_len_conduction))

        return temp_surf



class Fp_to_Fp(Temperature_calculation):

    def fp_to_fp(self,number_layer,temp_Tprev,temp_Tn,temp_Tnext):

        len_x_Tprev = Decimal(self.len_wh_TP[number_layer+1][0])
        len_y_Tprev = Decimal(self.len_wh_TP[number_layer+1][1])
        len_x_Tn = Decimal(self.len_wh_TP[number_layer+2][0])
        len_y_Tn = Decimal(self.len_wh_TP[number_layer+2][1])


        len_around_Tprev = Decimal  (self.len_around[number_layer+1])
        len_around_Tnext = Decimal  (self.len_around[number_layer+2])


        area_Tn =Decimal  (self.area_TS[number_layer+1])

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

        len_x_Term_prev = Decimal  (self.len_wh_TP[self.total_layer+1][0])
        len_y_Term_prev = Decimal  (self.len_wh_TP[self.total_layer+1][1])
        len_x_Term = Decimal  (self.len_wh_TP[self.total_layer+2][0])
        len_y_Term = Decimal  (self.len_wh_TP[self.total_layer+2][1])


        len_around_Term_prev = Decimal  (self.len_around[self.total_layer+1])

        area_Term = Decimal  (self.area_TS[self.total_layer+1])
        area_S = Decimal  (self.area_TS[self.total_layer+2])


        ther_conductivity_Term =Decimal  ( super().pf_ther_conductivity(self.temp_Term))
        ther_resistivity_Term = Decimal  (self.d_time / ((self.pf_density * self.pf_sh * area_Term) + (self.steel_density * steel_sh * area_S)))

        self.temp_Term = Decimal  (temp_Term + ther_resistivity_Term * (   len_around_Term_prev * ther_conductivity_Term / ((self.len_Tn / 2)+ self.len_Term)  )*(temp_Term_prev - temp_Term))

        return self.temp_Term
