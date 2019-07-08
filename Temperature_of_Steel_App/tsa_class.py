# -*- coding: utf-8 -*-
import math
import configparser


# 空のクラス
class TestTsa:
    test_value1 = 'None'
    test_value0 = 'クラス変数'

    def __init__(self, code, name):
        TestTsa.test_value2 = 2
        self.test_value1 = [[0] * 2] * 2
        self.test_value3 = 3
        print('インスタンスの' + self.test_value0)
        self.code = code
        self.name = name


# ini_fileからデータ読み取り
class LoadingInputValue:

    def __init__(self):

        ini_files = configparser.ConfigParser()
        ini_files.read('./tsa_config.ini', 'UTF-8')

        # save path
        LoadingInputValue.data_save_path = ini_files.get('settings', 'data_save_path')

        # test detail
        self.d_time = float(ini_files.get('settings', 'delta_time'))
        self.is_display_with_kelvin = bool(
            self.true_or_false('settings, display_Kelvin', ini_files.get('settings', 'display_Kelvin')))
        self.test_t = int(ini_files.get('settings', 'testing_time'))
        self.u_floor = bool(
            self.true_or_false('Test_Specimens , under_floor', ini_files.get('Test_Specimens', 'under_floor')))

        # test specimen
        self.type_Steel = ini_files.get('Test_Specimens', 'type_of_steel')
        self.type_FP = ini_files.get('Test_Specimens', 'type_of_Fireproofing')

        # test specimen detail
        self.width_steel = \
            float(ini_files.get('Test_Specimens', 'width_of_steel')) * (10 ** -3)
        self.height_steel = \
            float(ini_files.get('Test_Specimens', 'height_of_steel')) * (10 ** -3)
        self.thickness_Steel = \
            float(ini_files.get('Test_Specimens', 'thickness_of_steel')) * (10 ** -3)
        self.thickness_Steel_web = \
            float(ini_files.get('Test_Specimens', 'thickness_of_steel_web')) * (10 ** -3)
        self.thickness_Steel_flange = \
            float(ini_files.get('Test_Specimens', 'thickness_of_steel_flange')) * (10 ** -3)
        self.thickness_FP = \
            float(ini_files.get('Test_Specimens', 'thickness_of_Fireproofing')) * (10 ** -3)

        # 角形鋼材のみ
        self.width_inside_steel = self.width_steel - (2 * self.thickness_Steel)  # 角型鋼管中空幅
        self.height_inside_steel = self.height_steel - (2 * self.thickness_Steel)  # 角形鋼管中空高

        # layer detail
        self.total_layer = int(ini_files.get('Test_Specimens', 'number_of_layer'))
        self.len_surf = float(ini_files.get('Test_Specimens', 'thickness_of_Fireproofing_surface')) * (10 ** -3)
        self.len_Term = float(ini_files.get('Test_Specimens', 'thickness_of_Fireproofing_terminal')) * (10 ** -3)
        self.len_Tn = float((self.thickness_FP - self.len_surf - self.len_Term) / self.total_layer)  # 耐火被覆1層の厚

        # Default temperature
        self.temp_Default_furnace = float(ini_files.get('default-temperature', 'temperature_of_Furnace')) + 273
        self.temp_furnace = self.temp_Default_furnace
        self.temp_FP = float(ini_files.get('default-temperature', 'temperature_of_Fireproofing')) + 273
        self.temp_Steel = float(ini_files.get('default-temperature', 'temperature_of_Steel')) + 273

        # elements value
        self.emissivity_pf = float(ini_files.get('variable', 'emissivity_of_Fireproofing'))
        self.pf_specific_heat = float(ini_files.get('variable', 'specific_heat_of_Fireproofing'))
        self.pf_density = float(ini_files.get('variable', 'density_of_Fireproofing'))
        self.steel_density = float(ini_files.get('variable', 'density_of_Steel'))

    @staticmethod
    def true_or_false(jd_name, judge):
        if judge == "True":
            return True
        elif judge == "False":
            return False
        else:
            print(jd_name + 'Error')


# メインクラス
class TemperatureCalculation:

    # クラス変数

    # # 定数 以下の定数の値は仮
    # # 試験条件
    # DELTA_TIME = 0.1  # 単位時間
    # TESTING_TIME = 60  # 試験時間
    # IS_UNDER_FLOOR = False  # 試験体の床の有無
    #
    # # 鋼材仕様
    # TYPE_STEEL_MATERIAL = 'Void'  # 鋼材種類 H型or角形
    # WIDTH_STEEL = 10  # 鋼材幅
    # HEIGHT_STEEL = 10  # 鋼材背
    #
    # THICKNESS_STEEL_SQUARE = 10  # 角形鋼管鋼材厚
    # THICKNESS_STEEL_FLANGE = 5  # H型鋼フランジ厚
    # THICKNESS_STEEL_WEB = 10  # H型鋼ウェブ厚
    #
    # WIDTH_INSIDE_STEEL = 0  # 角型鋼管中空幅
    # HEIGHT_INSIDE_STEEL = 0  # 角形鋼管中空高
    #
    # DENSITY_STEEL = 7850  # 鋼材密度
    #
    # # 耐火被覆仕様
    # TYPE_FIREPROOF = 'Void'  # 耐火被覆材種
    # THICKNESS_FP = 10  # 耐火被覆厚
    #
    # SPECIFIC_HEAT_FIREPROOF = 1  # 耐火被覆比熱
    # DENSITY_FIREPROOF = 130  # 耐火被覆密度
    # EMISSIVITY_FIREPROOF = 0.97  # 耐火被覆放射率
    #
    # # 計算パラメータ
    # TOTAL_LAYER = 3  # 耐火被覆の計算層 +表面+端で+2
    # LEN_SURFACE = 2  # 表面厚
    # LEN_TERMINAL = 2  # 末端厚
    # THICKNESS_PER_LAYER = 2  # 耐火被覆一層あたりの厚さ
    # TOTAL_WIDTH_TEST_SPECIMEN = 30  # 試験体幅(鋼材幅+耐火被覆厚*2)
    # TOTAL_HEIGHT_TEST_SPECIMEN = 30  # 試験体背(鋼材背+耐火被覆厚*2)
    #
    # # 初期条件
    # TEMPERATURE_FURNACE_DEFAULT = 293  # 炉内温度 初期値
    # TEMPERATURE_FIREPROOF_DEFAULT = 293  # 炉内温度 初期値
    # TEMPERATURE_STEEL_DEFAULT = 293  # 鋼材温度 初期値
    #
    # # 変数 値は初期値
    # temperature_furnace = 293  # 炉内温度
    # array_thickness_fireproof = [0] * (TOTAL_LAYER+3)  # TOTAL LAYERを 代入してから とりあえず
    # array_len_width_height_test = [[0]*2] * (TOTAL_LAYER+3)
    # array_len_around = [0] * (TOTAL_LAYER+3)
    # array_area = [0] * (TOTAL_LAYER+3)

    # コンストラクタ クラス定数の初期値を代入
    def __init__(self, ini_input):

        # 試験条件
        self.delta_time = ini_input.d_time  # 単位時間
        self.testing_time = ini_input.test_t  # 試験時間
        self.is_under_floor = ini_input.u_floor  # 試験体の床の有無

        # 鋼材仕様
        self.type_steel_material = ini_input.type_Steel  # 鋼材種類 H型or角形
        self.width_steel = float(ini_input.width_steel)  # 鋼材幅
        self.height_steel = float(ini_input.height_steel)  # 鋼材背

        self.thickness_steel_square = ini_input.thickness_Steel  # 角形鋼管鋼材厚
        self.thickness_steel_flange = ini_input.thickness_Steel_flange  # H型鋼フランジ厚
        self.thickness_steel_web = ini_input.thickness_Steel_web  # H型鋼ウェブ厚

        self.width_inside_steel = ini_input.width_inside_steel  # 角型鋼管中空幅
        self.height_inside_steel = ini_input.height_inside_steel  # 角形鋼管中空高

        self.density_steel = ini_input.steel_density  # 鋼材密度

        # 耐火被覆仕様
        self.type_fireproof = ini_input.type_FP  # 耐火被覆材種
        self.thickness_fireproofing = ini_input.thickness_FP  # 耐火被覆厚

        self.specific_heat_fireproof = ini_input.pf_specific_heat  # 耐火被覆比熱
        self.density_fireproof = ini_input.pf_density  # 耐火被覆密度
        self.emissivity_fireproof = ini_input.emissivity_pf  # 耐火被覆放射率

        # 計算パラメーター
        self.total_layer = int(ini_input.total_layer)  # 耐火被覆の計算層 +表面+端で+2
        self.len_surface = ini_input.len_surf  # 表面厚
        self.len_terminal = ini_input.len_Term  # 末端厚
        self.thickness_per_layer = ini_input.len_Tn  # 耐火被覆一層あたりの厚さ

        # 初期条件
        self.temperature_furnace_default = ini_input.temp_Default_furnace  # 炉内温度 初期値
        # self.temperature_fireproof_default = ini_input.temp_FP  # 耐火被覆温度 初期値
        # self.temperature_steel_default = ini_input.temp_Steel  # 鋼材温度 初期値

        # インスタンス変数
        # self.temperature_furnace = ini_input.temp_furnace  # 炉内温度

        # インスタンス配列変数のリスト
        list_layer = ['furnace', 'surface']
        for i in range(self.total_layer):
            list_layer.append(i)
        list_layer.extend(['terminal', 'steel', 'inside_steel'])
        print(list_layer)
        self.list_name_layer = list_layer
        # ['furnace', 'surface', 0, 1, 2, 'terminal', 'steel', 'inside_steel']

        # 単位時間前の温度配列
        # [0.炉内, 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層, Total_Layer+3.鋼材]
        self.array_temperature_prevent = [0 for _ in self.list_name_layer]  # total_layer + 4 の配列を追加
        # 耐火被覆温度初期値 を追加
        for i, layer_name in enumerate(self.list_name_layer):
            if layer_name == 'furnace':
                self.array_temperature_prevent[i] = self.temperature_furnace_default  # 炉内温度 初期値 を代入
            elif layer_name == 'steel':
                self.array_temperature_prevent[i] = ini_input.temp_Steel  # 鋼材温度 初期値 を代入
            elif layer_name == 'inside_steel':
                self.array_temperature_prevent[i] = 'none'
            else:
                self.array_temperature_prevent[i] = ini_input.temp_FP  # 耐火被覆温度 初期値 を代入

        # 現在の温度配列(単位時間前の温度から計算し代入する)
        # [0.炉内, 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層, Total_Layer+3.鋼材]
        self.array_temperature = [0 for _ in self.list_name_layer]  # total_layer + 4 の配列を追加

        self.temperature_k = 20

        # 試験体全体幅高さ
        self.total_width_test_specimen = 0  # 試験体幅(鋼材幅+耐火被覆厚*2(or1))
        self.total_height_test_specimen = 0  # 試験体背(鋼材背+耐火被覆厚*2(or1))

        # 各層厚さ配列
        self.array_thickness = ['none', self.len_surface]
        for i in range(self.total_layer):
            self.array_thickness.append(self.thickness_per_layer)
        self.array_thickness.extend([self.len_terminal, 'none', 'none'])

        # 鋼材からの各層耐火被覆厚配列
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層 Total_Layer+3.鋼材]
        self.array_thickness_fireproof = [0 for _ in self.list_name_layer]

        # 耐火被覆縦横長さ
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,
        # Total_Layer+2.末端層, Total_Layer+3.鋼材, Total_Layer+4.鋼材内側(角形鋼管のみ)]
        self.array_len_width_height = [[0 for _ in range(2)] for _ in self.list_name_layer]

        # 各層の加熱外周囲
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,
        # Total_Layer+2.末端層, Total_Layer+3.鋼材, Total_Layer+4.鋼材内側(角形鋼管のみ)]
        self.array_len_around = [0 for _ in self.list_name_layer]

        # 各層の面積
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層, Total_Layer+3.鋼材]
        self.array_area = [0 for _ in self.list_name_layer]

        # 初期値代入
        self.cal_fp_thick()  # 各層耐火被覆厚計算 array_thickness_fireproof に代入
        self.assignment_len_width_height_tp()  # 各層耐火被覆縦横長さ計算 array_len_width_height に代入
        self.cal_len_around()  # 各層周囲長計算 array_len_around に代入
        # self.cal_area()  # 各層面積計算 array_area に代入

        # print(self.len_wh_TP)
        # print(fp_thick)
        # print(self.area_TS)
        # print(test)

        # self.fp_thick = [0 for i in range(self.total_layer + 3)]
        # self.cal_fp_thick()
        # self.len_wh_TP = [[0 for i in range(2)] for j in range(self.total_layer + 3)]
        # self.cal_len_wh_tp()
        # self.len_around = [0 for i in range(self.total_layer + 3)]
        # self.cal_len_around()
        # self.area_TS = [0 for i in range(self.total_layer + 3)]
        #
        # print(self.area_TS)

        # for i in range(self.total_layer + 3):
        #     print("thick==" + str(self.fp_thick[i]) + "\n")
        # for i in range(self.total_layer + 3):
        #     print("array==" + str(self.len_wh_TP[i]) + "\n")
        # for i in range(self.total_layer + 3):
        #     print("around==" + str(self.len_around[i]) + "\n")
        # for i in range(self.total_layer + 3):
        #     print("area==" + str(self.area_TS[i]) + "\n")

    #  耐火被覆の伝導率計算
    def pf_thermal_conductivity(self, temp):
        if self.type_fireproof == 'mineral_wool':
            self.temperature_k = float(temp)
            conductivity_pf = 6.71 * (10 ** -5)
        elif self.type_fireproof == 'ceramic_fiber':
            conductivity_pf = 0
            if temp < 400:
                conductivity_pf = 0.00009
            elif 400 <= temp < 800:
                conductivity_pf = \
                    ((((0.11 / 400) * temp) - 0.02) * (10 ** -3))
            elif temp >= 800:
                conductivity_pf = \
                    ((((0.09 / 200) * temp) - 0.16) * (10 ** -3))
            else:
                print('Fireproofing conductivity error : Temperature of ceramic_fiber is not collect')
        else:
            print('Fireproofing conductivity error : ' + self.type_fireproof + 'is not corresponded')
        return conductivity_pf

    #  ISO834加熱曲線
    def cal_temperature_furnace(self, times_seconds):
        times_minutes = times_seconds / 60
        temperature_furnace = 345 * math.log10(8 * times_minutes + 1) + self.temperature_furnace_default
        return temperature_furnace

    #  炉内最高温度(100K 切り上げ)
    def cal_temperature_max(self):
        temp_max = self.cal_temperature_furnace(self.testing_time * 60)
        temp_max = (temp_max // 100) * 100 + 100
        return temp_max

    # 各層耐火被覆厚計算
    def cal_fp_thick(self):
        for i, layer_name in enumerate(self.list_name_layer):
            if layer_name == 'furnace' or layer_name == 'inside_steel':
                self.array_thickness_fireproof[i] = 'none'
            elif layer_name == 'surface':
                self.array_thickness_fireproof[1] = self.thickness_fireproofing
            elif layer_name == 'steel':
                self.array_thickness_fireproof[i] = 0
            else:
                self.array_thickness_fireproof[i] = self.thickness_fireproofing - (
                        self.len_surface + self.thickness_per_layer * (i - 2))

    # 各層耐火被覆縦横長さ代入
    def assignment_len_width_height_tp(self):

        for i, name_layer in enumerate(self.list_name_layer):
            for j in range(2):
                if name_layer == 'furnace' or name_layer == 'inside_steel':
                    self.array_len_width_height[i][j] = 'none'
                else:
                    self.array_len_width_height[i][j] = self.cal_len_fireproofing_width_height(i, j)

    # -耐火被覆幅高長さ計算
    def cal_len_fireproofing_width_height(self, layer_number, width_or_height):

        coefficient_fp_cal = 2  # 床なし、試験大量側に耐火被覆 = 2

        if self.is_under_floor and width_or_height == 1:
            coefficient_fp_cal = 1  # 床付きの時、高さ方向片側耐火被覆なし = 1

        if width_or_height == 0:
            total_test_specimen = self.width_steel + (coefficient_fp_cal * self.thickness_fireproofing)
        elif width_or_height == 1:
            total_test_specimen = self.height_steel + (coefficient_fp_cal * self.thickness_fireproofing)
        else:
            print("Error:Unexpected number in width or height of def cal_len_fireproofing_width_height")
            return
        len_fp_width_height = total_test_specimen
        for i in range(layer_number):
            if i == 0:
                pass
            else:
                len_fp_width_height -= (self.array_thickness[i] * coefficient_fp_cal)
        return len_fp_width_height

    # 各層加熱周囲長計算
    def cal_len_around(self):
        coefficient_fp_cal = 2  # 床なし、試験大量側に耐火被覆 = 2
        if self.is_under_floor:
            coefficient_fp_cal = 1  # 床付きの時、高さ方向片側耐火被覆なし = 1

        if self.type_steel_material == 'square':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    pass
                else:
                    self.array_len_around[i] = (coefficient_fp_cal * self.array_len_width_height[i][0]) + (
                        2 * self.array_len_width_height[i][1])
        elif self.type_steel_material == 'H-beam':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    pass
                else:
                    self.array_len_around[i] = (coefficient_fp_cal * self.array_len_width_height[i][0]) + (
                            2 * self.array_len_width_height[i][1]) + (
                                                       2 * (self.width_steel - self.thickness_steel_web))
        else:
            print("Error : Unexpected string in type of steel material")

    # 角形鋼管 各層 面積計算
    def cal_area(self):
        if self.type_steel_material == 'square':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    pass
                else:
                    self.array_area[i] = self.array_len_width_height[i][0] * self.array_len_width_height[i][1] - \
                                     self.array_len_width_height[i + 1][0] * self.array_len_width_height[i + 1][1]

        elif self.type_steel_material == 'H-beam':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    pass
                else:
                    self.array_area[i] = self.cal_h_type_area(i) - self.cal_h_type_area(i + 1)
            self.array_area[self.total_layer + 2] = (2 * (self.width_steel *
                                                          self.thickness_steel_flange) + (
                                                             (self.height_steel - (
                                                                     2 * self.thickness_steel_flange)) *
                                                             self.thickness_steel_web))

    # H形鋼 各層 面積計算
    def cal_h_type_area(self, n_layer):
        h_area = (self.array_len_width_height[n_layer][0] * self.array_len_width_height[n_layer][1]) - (
                (self.height_steel - (2 * (self.array_thickness_fireproof[n_layer] + self.thickness_steel_flange))) * (
                self.width_steel - self.thickness_steel_web))

        return h_area

    # 外気から表面耐火被覆への温度計算
    # class SurfaceFireProofing(TemperatureCalculation):

    def surface_heat_transfer(self, temp_f, temp_surf):
        temp_f = temp_f
        self.heat_flux_convection = 0.023 * (temp_f - temp_surf)
        self.heat_flux_radiation = float(
            5.67 * (10 ** -11) * self.emissivity_fireproof * (float(temp_f ** 4) - float(temp_surf ** 4)))

    def surface_fp(self, temp_f, temp_surf, temp_t0):
        self.temp_t0 = temp_t0
        thermal_conductivity = TemperatureCalculation.pf_thermal_conductivity(temp_surf)
        self.surface_heat_transfer(temp_f, temp_surf)

        # len_x_surf = self.len_wh_TP[1][0]
        # len_y_surf = self.len_wh_TP[1][1]

        len_around_fp = self.array_len_around[0]
        len_around_inside_surf = self.array_len_around[1]
        area_surf = self.array_area[0]
        # area_surf = 0.1

        print(self.delta_time, self.density_fireproof, self.specific_heat_fireproof, area_surf)
        print(self.density_fireproof * self.specific_heat_fireproof * area_surf)

        thermal_resistivity_surf = self.delta_time / (
                self.density_fireproof * self.specific_heat_fireproof * area_surf)
        power_per_len_convection = len_around_fp * self.heat_flux_convection
        power_per_len_radiation = len_around_fp * self.heat_flux_radiation
        power_per_len_conduction = \
            len_around_inside_surf * (thermal_conductivity / (self.len_surface + (self.thickness_per_layer / 2))) * (
                    temp_t0 - temp_surf)
        temp_surf = temp_surf + thermal_resistivity_surf * (
                power_per_len_convection + power_per_len_radiation + power_per_len_conduction)
        return temp_surf


# 耐火被覆管の温度
class FpToFp(TemperatureCalculation):

    def fp_to_fp(self, number_layer, temperature_prev, temperature_layer, temperature_next):
        # len_x_prev = Decimal(self.len_wh_TP[number_layer + 1][0])
        # len_y_prev = Decimal(self.len_wh_TP[number_layer + 1][1])
        # len_x_tn = Decimal(self.len_wh_TP[number_layer + 2][0])
        # len_y_tn = Decimal(self.len_wh_TP[number_layer + 2][1])

        len_around_prev = self.array_len_around[number_layer + 1]
        len_around_next = self.array_len_around[number_layer + 2]

        area_tn = self.array_area[number_layer + 1]

        thermal_conductivity = TemperatureCalculation.pf_thermal_conductivity(temperature_layer)
        thermal_resistivity_tn = self.delta_time / (self.density_fireproof * self.specific_heat_fireproof * area_tn)
        power_per_len_conduction_prev = \
            len_around_prev * (
                    thermal_conductivity / ((self.thickness_per_layer / 2) + (self.thickness_per_layer / 2))) * (
                    temperature_prev - temperature_layer)
        power_per_len_conduction_next = \
            len_around_next * (
                    thermal_conductivity / ((self.thickness_per_layer / 2) + (self.thickness_per_layer / 2))) * (
                    temperature_next - temperature_layer)

        temperature_layer = \
            temperature_layer + thermal_resistivity_tn * (
                    power_per_len_conduction_prev + power_per_len_conduction_next)

        return temperature_layer


# 末端の耐火被覆の温度
class FpTerminal(TemperatureCalculation):

    @staticmethod
    def __steel_specific_heat(temp_steel):
        steel_sh = (0.482 + 8 * (10 ** -10) * ((temp_steel - 273) ** 2))
        return steel_sh

    def fp_terminal(self, temp_term_prev, temp_term):
        self.temp_term = temp_term
        steel_sh = self.__steel_specific_heat(temp_term)

        # len_x_Term_prev = Decimal(self.len_wh_TP[self.total_layer + 1][0])
        # len_y_Term_prev = Decimal(self.len_wh_TP[self.total_layer + 1][1])
        # len_x_Term = Decimal(self.len_wh_TP[self.total_layer + 2][0])
        # len_y_Term = Decimal(self.len_wh_TP[self.total_layer + 2][1])

        len_around_term_prev = self.array_len_around[self.total_layer + 1]

        area_term = self.array_area[self.total_layer + 1]
        area_s = self.array_area[self.total_layer + 2]

        thermal_conductivity_term = TemperatureCalculation.pf_thermal_conductivity(self.temp_term)
        thermal_resistivity_term = \
            self.delta_time / ((self.density_fireproof * self.specific_heat_fireproof * area_term) + (
                    self.density_steel * steel_sh * area_s))

        self.temp_term = (temp_term + thermal_resistivity_term * (
                len_around_term_prev * thermal_conductivity_term / (
                (self.thickness_per_layer / 2) + self.len_terminal)) * (
                                  temp_term_prev - temp_term))

        return self.temp_term


# 安定性調査
class StabilityAnalysis(TemperatureCalculation):

    def cal_stability_time(self, cal_temp):
        len_min = self.cal_min_len(self.thickness_per_layer, self.cal_min_len(cal_temp.len_surf, cal_temp.len_Term))
        print(len_min)
        stability_time = \
            cal_temp.pf_sh * cal_temp.pf_density * len_min ** 2 / 2 / self.pf_thermal_conductivity(cal_temp.tempMAX)
        exponential_10 = int(0)
        while stability_time // 1 == 0:
            stability_time = stability_time * 10
            exponential_10 = exponential_10 + 1
        print(stability_time, exponential_10)
        stability_time = (stability_time // 0.1) / 10
        self.stability_time = stability_time * (10 ** (-1 * exponential_10))

        return self.stability_time

    @staticmethod
    def cal_total_time(self, cal_temp):
        total_test_time = ((cal_temp.test_t * 60 / cal_temp.d_time) * 0.00002 * cal_temp.total_layer) / 3600
        return total_test_time

    @staticmethod
    def cal_min_len(a, b):
        if a <= b:
            return a
        else:
            return b
