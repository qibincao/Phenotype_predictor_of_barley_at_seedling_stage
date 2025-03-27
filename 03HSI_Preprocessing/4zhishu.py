import pandas as pd
import numpy as np
import os
# 定义文件夹路径
input_folder = 'bandout'  # 输入文件夹
input_file = os.path.join(input_folder, 'average_reflectance.csv')  # 输入文件路径

# 新的列名
new_columns = [
    "File Name", "397.32", "400.2", "403.09", "405.97", "408.85", "411.74", "414.63", "417.52", "420.4",
    "423.29", "426.19", "429.08", "431.97", "434.87", "437.76", "440.66", "443.56", "446.45", "449.35",
    "452.25", "455.16", "458.06", "460.96", "463.87", "466.77", "469.68", "472.59", "475.5", "478.41",
    "481.32", "484.23", "487.14", "490.06", "492.97", "495.89", "498.8", "501.72", "504.64", "507.56",
    "510.48", "513.4", "516.33", "519.25", "522.18", "525.1", "528.03", "530.96", "533.89", "536.82",
    "539.75", "542.68", "545.62", "548.55", "551.49", "554.43", "557.36", "560.3", "563.24", "566.18",
    "569.12", "572.07", "575.01", "577.96", "580.9", "583.85", "586.8", "589.75", "592.7", "595.65",
    "598.6", "601.55", "604.51", "607.46", "610.42", "613.38", "616.34", "619.3", "622.26", "625.22",
    "628.18", "631.15", "634.11", "637.08", "640.04", "643.01", "645.98", "648.95", "651.92", "654.89",
    "657.87", "660.84", "663.81", "666.79", "669.77", "672.75", "675.73", "678.71", "681.69", "684.67",
    "687.65", "690.64", "693.62", "696.61", "699.6", "702.58", "705.57", "708.57", "711.56", "714.55",
    "717.54", "720.54", "723.53", "726.53", "729.53", "732.53", "735.53", "738.53", "741.53", "744.53",
    "747.54", "750.54", "753.55", "756.56", "759.56", "762.57", "765.58", "768.6", "771.61", "774.62",
    "777.64", "780.65", "783.67", "786.68", "789.7", "792.72", "795.74", "798.77", "801.79", "804.81",
    "807.84", "810.86", "813.89", "816.92", "819.95", "822.98", "826.01", "829.04", "832.07", "835.11",
    "838.14", "841.18", "844.22", "847.25", "850.29", "853.33", "856.37", "859.42", "862.46", "865.5",
    "868.55", "871.6", "874.64", "877.69", "880.74", "883.79", "886.84", "889.9", "892.95", "896.01",
    "899.06", "902.12", "905.18", "908.24", "911.3", "914.36", "917.42", "920.48", "923.55", "926.61",
    "929.68", "932.74", "935.81", "938.88", "941.95", "945.02", "948.1", "951.17", "954.24", "957.32",
    "960.4", "963.47", "966.55", "969.63", "972.71", "975.79", "978.88", "981.96", "985.05", "988.13",
    "991.22", "994.31", "997.4", "1000.49", "1003.58"
]

# 读取原始表格数据
df = pd.read_csv(input_file)

# 替换列名为新的列名
df.columns = new_columns

# 提取波长信息，将列名转换为浮点数
wavelength_columns = [float(col) for col in df.columns[1:]]  # 第一列是文件名，其余列是波长
wavelength_dict = {float(col): col for col in df.columns[1:]}  # 创建波长到列名的映射

# 定义一个函数，用于查找最接近的波长列
def find_closest_wavelength(target_wavelength, wavelengths):
    return min(wavelengths, key=lambda x: abs(x - target_wavelength))

# 定义植被指数计算函数
def calculate_vegetation_indices(df, wavelengths, wavelength_dict):
    # RD: R705 - R505
    closest_705 = find_closest_wavelength(705, wavelengths)
    closest_505 = find_closest_wavelength(505, wavelengths)
    df['RD'] = df[wavelength_dict[closest_705]] - df[wavelength_dict[closest_505]]

    # mSR705: (R750 - R445) / (R705 - R445)
    closest_750 = find_closest_wavelength(750, wavelengths)
    closest_445 = find_closest_wavelength(445, wavelengths)
    df['mSR705'] = (df[wavelength_dict[closest_750]] - df[wavelength_dict[closest_445]]) / \
                   (df[wavelength_dict[closest_705]] - df[wavelength_dict[closest_445]])

    # mNDVI: (R750 - R705) / (R750 + R705 - 2R445)
    df['mNDVI'] = (df[wavelength_dict[closest_750]] - df[wavelength_dict[closest_705]]) / \
                  (df[wavelength_dict[closest_750]] + df[wavelength_dict[closest_705]] - 2 * df[wavelength_dict[closest_445]])

    # TCARI: 3 * [(R700 - R670) - 0.2 * (R700 - R550) * (R700 / R670)]
    closest_700 = find_closest_wavelength(700, wavelengths)
    closest_670 = find_closest_wavelength(670, wavelengths)
    closest_550 = find_closest_wavelength(550, wavelengths)
    df['TCARI'] = 3 * ((df[wavelength_dict[closest_700]] - df[wavelength_dict[closest_670]]) - 
                       0.2 * (df[wavelength_dict[closest_700]] - df[wavelength_dict[closest_550]]) * 
                       (df[wavelength_dict[closest_700]] / df[wavelength_dict[closest_670]]))

    # NDCI: (R762 - R527) / (R762 + R527)
    closest_762 = find_closest_wavelength(762, wavelengths)
    closest_527 = find_closest_wavelength(527, wavelengths)
    df['NDCI'] = (df[wavelength_dict[closest_762]] - df[wavelength_dict[closest_527]]) / \
                 (df[wavelength_dict[closest_762]] + df[wavelength_dict[closest_527]])

    # NDVI1: (R780 - R550) / (R780 + R550)
    closest_780 = find_closest_wavelength(780, wavelengths)
    df['NDVI1'] = (df[wavelength_dict[closest_780]] - df[wavelength_dict[closest_550]]) / \
                  (df[wavelength_dict[closest_780]] + df[wavelength_dict[closest_550]])

    # NPQI: (R415 - R435) / (R415 + R435)
    closest_415 = find_closest_wavelength(415, wavelengths)
    closest_435 = find_closest_wavelength(435, wavelengths)
    df['NPQI'] = (df[wavelength_dict[closest_415]] - df[wavelength_dict[closest_435]]) / \
                 (df[wavelength_dict[closest_415]] + df[wavelength_dict[closest_435]])

    # NDVI705: (R750 - R705) / (R750 + R705)
    df['NDVI705'] = (df[wavelength_dict[closest_750]] - df[wavelength_dict[closest_705]]) / \
                    (df[wavelength_dict[closest_750]] + df[wavelength_dict[closest_705]])

    # REP: 700 + 40 * ((R670 + R780) / 2 - R700) / (R740 - R700)
    closest_670 = find_closest_wavelength(670, wavelengths)
    closest_780 = find_closest_wavelength(780, wavelengths)
    closest_740 = find_closest_wavelength(740, wavelengths)
    df['REP'] = 700 + 40 * ((df[wavelength_dict[closest_670]] + df[wavelength_dict[closest_780]]) / 2 - 
                            df[wavelength_dict[closest_700]]) / (df[wavelength_dict[closest_740]] - df[wavelength_dict[closest_700]])

    # SR1: R415 / R710
    closest_710 = find_closest_wavelength(710, wavelengths)
    df['SR1'] = df[wavelength_dict[closest_415]] / df[wavelength_dict[closest_710]]

    # SR2: R675 / (R700 * R650)
    closest_675 = find_closest_wavelength(675, wavelengths)
    closest_650 = find_closest_wavelength(650, wavelengths)
    df['SR2'] = df[wavelength_dict[closest_675]] / (df[wavelength_dict[closest_700]] * df[wavelength_dict[closest_650]])

    # SR3: R860 / (R550 * R708)
    closest_860 = find_closest_wavelength(860, wavelengths)
    closest_708 = find_closest_wavelength(708, wavelengths)
    df['SR3'] = df[wavelength_dict[closest_860]] / (df[wavelength_dict[closest_550]] * df[wavelength_dict[closest_708]])

    # MTCI: (R750 - R710) / (R710 - R680)
    closest_680 = find_closest_wavelength(680, wavelengths)
    df['MTCI'] = (df[wavelength_dict[closest_750]] - df[wavelength_dict[closest_710]]) / \
                 (df[wavelength_dict[closest_710]] - df[wavelength_dict[closest_680]])

    # GNDVI: (R750 - R550) / (R750 + R550)
    df['GNDVI'] = (df[wavelength_dict[closest_750]] - df[wavelength_dict[closest_550]]) / \
                  (df[wavelength_dict[closest_750]] + df[wavelength_dict[closest_550]])

    # GNDVI2: (R801 - R550) / (R801 + R550)
    closest_801 = find_closest_wavelength(801, wavelengths)
    df['GNDVI2'] = (df[wavelength_dict[closest_801]] - df[wavelength_dict[closest_550]]) / \
                   (df[wavelength_dict[closest_801]] + df[wavelength_dict[closest_550]])

    # DCNI: (R720 - R700) / (R700 - R670) / (R720 - R670 + 0.03)
    closest_720 = find_closest_wavelength(720, wavelengths)
    df['DCNI'] = (df[wavelength_dict[closest_720]] - df[wavelength_dict[closest_700]]) / \
                 (df[wavelength_dict[closest_700]] - df[wavelength_dict[closest_670]]) / \
                 (df[wavelength_dict[closest_720]] - df[wavelength_dict[closest_670]] + 0.03)

    # TCI: 1.2 * (R700 - R550) - 1.5 * (R670 - R550) * (R700 / R670)
    df['TCI'] = 1.2 * (df[wavelength_dict[closest_700]] - df[wavelength_dict[closest_550]]) - \
                1.5 * (df[wavelength_dict[closest_670]] - df[wavelength_dict[closest_550]]) * \
                (df[wavelength_dict[closest_700]] / df[wavelength_dict[closest_670]])

    # LCI: (R850 - R710) / (R850 + R680)
    closest_850 = find_closest_wavelength(850, wavelengths)
    df['LCI'] = (df[wavelength_dict[closest_850]] - df[wavelength_dict[closest_710]]) / \
                (df[wavelength_dict[closest_850]] + df[wavelength_dict[closest_680]])

    return df

# 计算植被指数
df_with_indices = calculate_vegetation_indices(df, wavelength_columns, wavelength_dict)

# 保存结果到新的表格
output_file = "vegetation_indices_table.csv"
df_with_indices.to_csv(output_file, index=False)
print(f"植被指数特征提取完成，结果已保存到 {output_file}")