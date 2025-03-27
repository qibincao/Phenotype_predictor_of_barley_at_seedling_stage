import pandas as pd
import joblib

# 读取 vegetation_indices_table.csv 文件
input_file = 'vegetation_indices_table.csv'
df = pd.read_csv(input_file)

# 预处理数据
# 删除第二列到第 205 列，保留第一列和第 206 列到第 223 列
# 假设第一列是索引列或文件名
processed_df = pd.concat([df.iloc[:, 0], df.iloc[:, 205:]], axis=1)

# 加载保存的模型
model_path = 'best_model_K-Nearest Neighbors.joblib'
model = joblib.load(model_path)

# 使用模型进行预测
# 假设第一列是索引列或文件名，不作为特征输入
X_predict = processed_df.iloc[:, 1:]  # 特征列
y_pred = model.predict(X_predict)

# 将预测结果添加到 DataFrame 中
processed_df['Prediction'] = y_pred

# 保存预测结果
output_file = 'prediction_results.csv'
processed_df.to_csv(output_file, index=False)
print(f"预测完成，结果已保存到 {output_file}")