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
        self.temperature_steel_default = ini_input.temp_Steel  # 鋼材温度 初期値

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
                self.array_temperature_prevent[i] = self.temperature_steel_default  # 鋼材温度 初期値 を代入
            elif layer_name == 'inside_steel':
                self.array_temperature_prevent[i] = 0
            else:
                self.array_temperature_prevent[i] = ini_input.temp_FP  # 耐火被覆温度 初期値 を代入

        # 現在の温度配列(単位時間前の温度から計算し代入する)
        # [0.炉内, 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層, Total_Layer+3.鋼材]
        self.array_temperature = [0 for _ in self.list_name_layer]  # total_layer + 4 の配列を追加

        self.temperature_k = 20

        # 試験体全体幅高さ -------------------------------------
        self.total_width_test_specimen = 0  # 試験体幅(鋼材幅+耐火被覆厚*2(or1))
        self.total_height_test_specimen = 0  # 試験体背(鋼材背+耐火被覆厚*2(or1))

        # 各層厚さ配列
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,
        # Total_Layer+2.末端層, Total_Layer+3.鋼材, Total_Layer+4.鋼材内側(角形鋼管のみ)]
        self.array_thickness = ['none', self.len_surface]
        for i in range(self.total_layer):
            self.array_thickness.append(self.thickness_per_layer)
        self.array_thickness.extend([self.len_terminal, 'none', 'none'])

        # 鋼材からの各層耐火被覆厚配列
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層 Total_Layer+3.鋼材]
        self.array_thickness_fireproof = ['none' for _ in self.list_name_layer]

        # 耐火被覆縦横長さ
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,
        # Total_Layer+2.末端層, Total_Layer+3.鋼材, Total_Layer+4.鋼材内側(角形鋼管のみ)]
        self.array_len_width_height = [['none' for _ in range(2)] for _ in self.list_name_layer]

        # 各層の加熱外周囲
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,
        # Total_Layer+2.末端層, Total_Layer+3.鋼材, Total_Layer+4.鋼材内側(角形鋼管のみ)]
        self.array_len_around = ['none' for _ in self.list_name_layer]

        # 各層の面積
        # [0.None 1.表面層, 2.層0, 3.層1, Layer_number+2.層2…,Total_Layer+2.末端層, Total_Layer+3.鋼材]
        self.array_area = ['none' for _ in self.list_name_layer]

        # 初期値代入
        self.cal_fp_thick()  # 各層耐火被覆厚計算 array_thickness_fireproof に代入
        self.assignment_len_width_height_tp()  # 各層耐火被覆縦横長さ計算 array_len_width_height に代入
        self.cal_len_around()  # 各層周囲長計算 array_len_around に代入
        self.cal_area()  # 各層面積計算 array_area に代入

    # 試験入力値表示
    def display_input(self, is_round):
        list_display = []
        for i, name in enumerate(self.list_name_layer):
            len_list = 15 - len(str(name))
            list_input_str = " " * len_list + str(name) + ":"
            list_display.append(list_input_str)

        print("\n各層厚さ配列")
        if is_round:
            for i, element in enumerate(self.array_thickness):
                if type(element) is str:
                    n_element = element
                else:
                    n_element = round(float(element), 5)
                print(list_display[i], n_element)
        else:
            for i, element in enumerate(self.array_thickness):
                print(list_display[i], element)

        print("\n鋼材からの各層耐火被覆厚配列")
        if is_round:
            for i, element in enumerate(self.array_thickness_fireproof):
                if type(element) is str:
                    n_element = element
                else:
                    n_element = round(float(element), 5)
                print(list_display[i], n_element)
        else:
            for i, element in enumerate(self.array_thickness_fireproof):
                print(list_display[i], element)

        print("\n耐火被覆縦横長さ")
        if is_round:
            for i in range(len(self.list_name_layer)):
                element = [self.array_len_width_height[i][0], self.array_len_width_height[i][1]]
                n_element = [0, 0]
                for j in range(2):
                    if type(element[j]) is str:
                        n_element[j] = element[j]
                    else:
                        n_element[j] = round(float(element[j]), 5)
                len_str = 7 - len(str(n_element[0]))
                print(list_display[i], n_element[0], " " * len_str, n_element[1])
        else:
            for i in range(len(self.list_name_layer)):
                len_str = 20 - len(str(self.array_len_width_height[i][0]))
                print(list_display[i], self.array_len_width_height[i][0], " " * len_str,
                      self.array_len_width_height[i][1])

        print("\n各層の加熱外周囲")
        if is_round:
            for i, element in enumerate(self.array_len_around):
                if type(element) is str:
                    n_element = element
                else:
                    n_element = round(float(element), 5)
                print(list_display[i], n_element)
        else:
            for i, element in enumerate(self.array_len_around):
                print(list_display[i], element)

        print("\n各層の面積")
        if is_round:
            for i, element in enumerate(self.array_area):
                if type(element) is str:
                    n_element = element
                else:
                    n_element = round(float(element), 5)
                print(list_display[i], n_element)
        else:
            for i, element in enumerate(self.array_area):
                print(list_display[i], element)

    # 試験入力値を並べて表示
    def display_input_column(self):
        list_display = []
        for i, name in enumerate(self.list_name_layer):
            len_list = 15 - len(str(name))
            list_input_str = " " * len_list + str(name) + ":"
            list_display.append(list_input_str)

        message_line = "{0} {1} {2} {3} {4} {5} {6}"
        print(message_line.format("          layer:", "think_L   ", "think_FP  ", "len_width ", "len_height",
                                  "len_around", "area      "))
        for i in range(len(self.list_name_layer)):
            n_element = [0, 0, 0, 0, 0, 0]
            for j, name in enumerate(
                    [self.array_thickness[i], self.array_thickness_fireproof[i], self.array_len_width_height[i][0],
                     self.array_len_width_height[i][1], self.array_len_around[i], self.array_area[i]]):
                if type(name) is str:
                    n_element[j] = name
                else:
                    n_element[j] = round(float(name), 8)
                len_str = 10 - len(str(n_element[j]))
                n_element[j] = str(n_element[j]) + " " * len_str
            print(message_line.format(list_display[i], n_element[0], n_element[1], n_element[2], n_element[3],
                                      n_element[4], n_element[5]))

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
            conductivity_pf = "Error"
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
            else:
                self.array_thickness_fireproof[i] = self.thickness_fireproofing - (
                        self.len_surface + self.thickness_per_layer * (i - 2))

    # 各層耐火被覆縦横長さ代入
    def assignment_len_width_height_tp(self):

        for i, layer_name in enumerate(self.list_name_layer):
            for j in range(2):
                if layer_name == 'furnace':
                    self.array_len_width_height[i][j] = 'none'
                elif layer_name == 'inside_steel':
                    if self.type_steel_material == 'square':
                        self.array_len_width_height[i][0] = self.width_steel - (2 * self.thickness_steel_square)
                        self.array_len_width_height[i][1] = self.height_steel - (2 * self.thickness_steel_square)
                    else:
                        self.array_len_width_height[i][j] = 'none'
                else:
                    self.array_len_width_height[i][j] = self.cal_len_fireproofing_width_height(i, j)

    # 耐火被覆幅高長さ計算
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
                if layer_name == 'furnace':
                    self.array_len_around[i] = 'none'
                elif layer_name == 'inside_steel':
                    if self.type_steel_material == 'square':
                        self.array_len_around[i] = (
                                2 * self.array_len_width_height[i][0] + 2 * self.array_len_width_height[i][1])
                    else:
                        self.array_len_around[i] = 'none'
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

    # 各層 面積計算
    def cal_area(self):
        if self.type_steel_material == 'square':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    self.array_area[i] = 'none'
                elif layer_name == 'steel':
                    self.array_area[i] = self.width_steel * self.height_steel - (
                            is_float(self.array_len_width_height[i + 1][0]) * is_float(
                        self.array_len_width_height[i + 1][1]))
                else:
                    self.array_area[i] = (is_float(self.array_len_around[i]) + is_float(
                        self.array_len_around[i + 1])
                                          ) / 2 * self.array_thickness[i]

        elif self.type_steel_material == 'H-beam':
            for i, layer_name in enumerate(self.list_name_layer):
                if layer_name == 'furnace' or layer_name == 'inside_steel':
                    self.array_area[i] = 'none'
                else:
                    self.array_area[i] = self.cal_h_type_area(i, layer_name)

    # H形鋼 各層 面積計算
    def cal_h_type_area(self, layer_number, layer_name):
        if layer_name == 'steel':
            area_h_beam = self.thickness_steel_flange * self.width_steel * 2 + (
                    self.thickness_steel_web * (self.height_steel - (2 * self.thickness_steel_flange)))
        elif layer_name == 'furnace' or layer_name == 'inside_steel':
            print("Error : Unexpected name in cal_h_type_area")
            area_h_beam = 'Error'
        else:
            area_h_beam = (is_float(self.array_len_around[layer_number]) + is_float(
                self.array_len_around[layer_number + 1])) / 2 * \
                          self.array_thickness[layer_number]
        return area_h_beam

    # 現在温度を計算
    def cal_new_temperature_array(self, current_time_seconds):

        self.array_temperature[0] = self.cal_temperature_furnace(current_time_seconds)  # 炉内温度を代入
        self.array_temperature[1] = self.surface_fp(self.array_temperature_prevent[0],
                                                    self.array_temperature_prevent[1],
                                                    self.array_temperature_prevent[2])
        terminal_layer_number = self.list_name_layer.index('terminal')
        for i in range(2, terminal_layer_number):
            self.array_temperature[i] = \
                self.fp_to_fp(i,
                              self.array_temperature_prevent[i - 1],
                              self.array_temperature_prevent[i],
                              self.array_temperature_prevent[i + 1])
        self.array_temperature[terminal_layer_number] = \
            self.fp_terminal(terminal_layer_number,
                             self.array_temperature_prevent[
                                 terminal_layer_number - 1],
                             self.array_temperature_prevent[
                                 terminal_layer_number])

    # 外気から表面耐火被覆への温度計算
    def surface_fp(self, temperature_furnace, temperature_surface, temperature_layer_0):

        thermal_conductivity_pf = self.pf_thermal_conductivity(temperature_surface)
        heat_flux = self.surface_heat_transfer(temperature_furnace, temperature_surface)
        heat_flux_convection = heat_flux[0]
        heat_flux_radiation = heat_flux[1]

        len_around_surface = self.array_len_around[1]
        len_around_inside_surface = self.array_len_around[2]
        area_surface = self.array_area[1]

        print(self.delta_time, self.density_fireproof, self.specific_heat_fireproof, area_surface)
        print(self.density_fireproof * self.specific_heat_fireproof * area_surface)

        thermal_resistivity_surf = self.delta_time / (
                self.density_fireproof * self.specific_heat_fireproof * area_surface)

        power_per_len_convection = len_around_surface * heat_flux_convection
        power_per_len_radiation = float(len_around_surface) * heat_flux_radiation
        power_per_len_conduction = \
            len_around_inside_surface * (
                    thermal_conductivity_pf / (self.array_thickness[1] + (self.array_thickness[2] / 2))) * (
                    temperature_surface - temperature_layer_0)

        temperature_surface_new = temperature_surface + \
                                  thermal_resistivity_surf * (
                                          power_per_len_convection + power_per_len_radiation - power_per_len_conduction)
        return temperature_surface_new

    def surface_heat_transfer(self, temperature_furnace, temperature_surface):
        temperature_furnace = temperature_furnace
        heat_flux_convection = 0.023 * (temperature_furnace - temperature_surface)
        heat_flux_radiation = float(
            5.67 * (10 ** -11) * self.emissivity_fireproof * (
                    float(temperature_furnace ** 4) - float(temperature_surface ** 4)))
        return heat_flux_convection, heat_flux_radiation

    # 耐火被覆管の温度
    def fp_to_fp(self, layer_number, temperature_prev, temperature_layer, temperature_next):
        len_around_prev = self.array_len_around[layer_number - 1]
        len_around_next = self.array_len_around[layer_number + 1]

        area_this_layer = self.array_area[layer_number]

        thermal_conductivity = self.pf_thermal_conductivity(temperature_layer)

        thermal_resistivity_this = self.delta_time / (
                self.density_fireproof * self.specific_heat_fireproof * area_this_layer)

        power_per_len_conduction_prev = \
            len_around_prev * (
                    thermal_conductivity / ((self.array_thickness[layer_number - 1] / 2) + (
                    self.array_thickness[layer_number] / 2))) * (
                    temperature_prev - temperature_layer)
        power_per_len_conduction_next = \
            len_around_next * (
                    thermal_conductivity / ((self.array_thickness[layer_number] / 2) + (
                    self.array_thickness[layer_number + 1] / 2))) * (
                    temperature_layer - temperature_next)

        temperature_layer_new = temperature_layer + \
                                thermal_resistivity_this * (
                                        power_per_len_conduction_prev - power_per_len_conduction_next)

        return temperature_layer_new

    # 末端の耐火被覆の温度
    def fp_terminal(self, terminal_layer_number, temperature_terminal_prev, temperature_terminal):

        steel_specific_heat = self.steel_specific_heat(temperature_terminal)

        len_around_terminal = self.array_len_around[terminal_layer_number]

        area_terminal = self.array_area[terminal_layer_number]
        area_steel = self.array_area[terminal_layer_number + 1]

        thermal_conductivity_terminal = self.pf_thermal_conductivity(temperature_terminal)

        thermal_resistivity_terminal = \
            self.delta_time / ((self.density_fireproof * self.specific_heat_fireproof * area_terminal) + (
                    self.density_steel * steel_specific_heat * area_steel))

        power_per_len_conduction_terminal = len_around_terminal * thermal_conductivity_terminal / (
                (self.array_thickness[terminal_layer_number - 1] / 2) + self.array_thickness[terminal_layer_number])

        temperature_terminal_now = temperature_terminal + \
                                   thermal_resistivity_terminal * power_per_len_conduction_terminal * (
                                           temperature_terminal_prev - temperature_terminal)
        return temperature_terminal_now

    @staticmethod
    def steel_specific_heat(temperature_steel):
        # steel_sh = (0.482 + 8 * (10 ** -10) * ((temperature_steel - 273) ** 2))

        temperature_steel_celsius = temperature_steel - 273
        if 0 <= temperature_steel_celsius < 600:
            steel_sh = 425 + (7.73 * (10 ** -1) * temperature_steel_celsius) - (
                    1.69 * (10 ** -3) * temperature_steel_celsius ** 2) + (2.22 * (
                    10 ** -6) * temperature_steel_celsius ** 3)
        elif 600 <= temperature_steel_celsius < 735:
            steel_sh = 666 + 13002 / (738 - temperature_steel_celsius)
        elif 735 <= temperature_steel_celsius < 900:
            steel_sh = 545 + 17820 / (temperature_steel_celsius - 731)
        elif 900 <= temperature_steel_celsius < 1200:
            steel_sh = 650
        else:
            print("Error : ", temperature_steel_celsius, "is unexpected value in temperature of steel")
            steel_sh = "Error"

        steel_specific_heat = float(is_float(steel_sh)) * (10 ** -3)

        return steel_specific_heat

    # 安定性調査
    def cal_stability_time(self):
        len_min = cal_min_array(self.array_thickness)
        #  max_temperature = self.cal_temperature_max()
        min_temperature = self.temperature_furnace_default
        stability_time_fireproofing = \
            self.specific_heat_fireproof * self.density_fireproof * (len_min ** 2) / 2 / self.pf_thermal_conductivity(
                min_temperature)
        stability_time_steel = 100
        # stability_time_steel = \
        #     self.steel_specific_heat(self.temperature_steel_default) * self.density_steel * (
        #                 len_min ** 2) / 2 / 1

        print("pf", stability_time_fireproofing, " steel", stability_time_steel)
        stability_time = cal_min_len(stability_time_fireproofing, stability_time_steel)

        exponential_10 = int(0)
        while stability_time // 1 == 0:
            stability_time = stability_time * 10
            exponential_10 = exponential_10 + 1
        print(stability_time, exponential_10)
        stability_time = (stability_time // 0.1) / 10
        stability_time = stability_time * (10 ** (-1 * exponential_10))
        stability_time = round(stability_time, exponential_10 + 1)

        return stability_time

    @staticmethod
    def cal_total_time(cal_temp):
        total_test_time = ((cal_temp.test_t * 60 / cal_temp.d_time) * 0.00002 * cal_temp.total_layer) / 3600
        return total_test_time


# functions

# floatに変換できないstrをエラーする
def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return s


def cal_min_len(a, b):
    if a <= b:
        return a
    else:
        return b


def cal_min_array(array):
    min_element = 10000
    for element in array:
        if type(element) is int or type(element) is float:
            min_element = cal_min_len(min_element, element)
    return min_element
