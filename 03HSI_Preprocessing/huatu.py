import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('test_data.csv')

# 设置字体为 Times New Roman，并增大字体大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16  # 增大字体大小

# 获取真实值和预测值
y_true = data['spad'].values
y_pred = data['Prediction'].values

# 计算 R² 和 RMSE
r2 = r2_score(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(y_true, y_pred, alpha=0.6, color='blue', label='Predicted vs True')

# 添加对角线
plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], color='red', linestyle='--')

# 添加标题和标签
plt.title('SPAD Prediction vs True Values', fontsize=18)
plt.xlabel('True Values', fontsize=16)
plt.ylabel('Predicted Values', fontsize=16)

# 添加图注，标记 R² 和 RMSE
plt.legend([f'R²: {r2:.3f}, RMSE: {rmse:.3f}'], loc='upper left', fontsize=14)

# 调整布局
plt.tight_layout()

# 显示图像
plt.show()

# 打印 R² 和 RMSE
print(f"R²: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")