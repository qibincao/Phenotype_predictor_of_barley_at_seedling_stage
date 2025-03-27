import numpy as np
import pandas as pd
import os
import glob
import rasterio

# 定义文件夹路径
input_folder = 'input'  # 高光谱图像文件夹
txtoutput_folder = 'txtoutput'  # 点坐标文件夹
output_folder = 'bandout'  # 输出文件夹

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取所有.dat文件的路径，包括子文件夹
file_paths = glob.glob(os.path.join(input_folder, '**', '*.dat'), recursive=True)

# 定义一个函数，用于从txt文件中读取点信息
def read_points_from_txt(txt_file):
    points = {}
    with open(txt_file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:  # 跳过空行
                continue
            parts = line.split(',')
            if len(parts) != 3:
                print(f"Warning: Line {line_number} in {txt_file} does not have 3 parts. Skipping.")
                continue
            file_name = parts[0].strip().replace('.jpg', '')  # 去掉.jpg扩展名
            try:
                x = int(parts[1].strip())
                y = int(parts[2].strip())
            except ValueError:
                print(f"Warning: Line {line_number} in {txt_file} has invalid coordinates. Skipping.")
                continue
            points[file_name] = (x, y)
    return points

# 读取txtoutput文件夹下的三个txt文件
txt_files = sorted(glob.glob(os.path.join(txtoutput_folder, 'points_*.txt')))

# 初始化一个列表，用于存储每个txt文件对应的DataFrame
all_data_list = []

# 遍历每个txt文件
for txt_file in txt_files:
    # 提取点信息
    points = read_points_from_txt(txt_file)
    all_data = pd.DataFrame()

    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]  # 获取不带扩展名的文件名

        # 如果当前文件名在点信息中
        if file_name in points:
            x, y = points[file_name]

            # 使用rasterio打开图像
            with rasterio.open(file_path) as src:
                image_data = src.read()  # 读取所有波段的数据

                # 提取该点的所有波段反射率
                reflectance_at_fixed_point = image_data[:, y - 1, x - 1]  # 索引从0开始

                # 将波段反射率和文件名添加到DataFrame
                df = pd.DataFrame([reflectance_at_fixed_point],
                                  columns=[f'Band_{i + 1}' for i in range(image_data.shape[0])])
                df.insert(0, 'File Name', file_name)
                all_data = pd.concat([all_data, df], ignore_index=True)

                # 打印文件名提示已完成
                print(f"{file_name} 已完成")

    # 保存当前txt文件对应的反射率数据到CSV
    csv_file = os.path.join(output_folder, os.path.basename(txt_file).replace('.txt', '.csv'))
    all_data.to_csv(csv_file, index=False, header=True)
    all_data_list.append(all_data)

# 计算每个波段的平均反射率
if all_data_list:
    # 确保所有DataFrame的形状一致
    for df in all_data_list:
        assert df.shape == all_data_list[0].shape, "DataFrames have different shapes."

    # 按列（波段）计算平均值
    avg_data = pd.concat(all_data_list).groupby('File Name').mean().reset_index()
    avg_data.to_csv(os.path.join(output_folder, 'average_reflectance.csv'), index=False, header=True)
    print("平均反射率已保存到 average_reflectance.csv")
else:
    print("没有找到任何数据。")