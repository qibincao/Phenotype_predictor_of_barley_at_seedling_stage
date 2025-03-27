import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import joblib  # 用于保存模型

# 导入数据
df = pd.read_csv('train_data.csv')

# 定义特征变量和目标变量
X = df.iloc[:, 1:-1]  # 从第二列到倒数第二列作为特征变量
y = df.iloc[:, -1]   # 目标变量

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# 初始化模型
models = {
    'Linear Regression': LinearRegression(),  # 多元线性回归
    'Ridge Regression': Ridge(alpha=1.0),  # 岭回归
    'Elastic Net': ElasticNet(alpha=0.1, l1_ratio=0.5),  # 弹性网络回归
    'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=5),  # K近邻回归
    'Bayesian Ridge': BayesianRidge(),  # 贝叶斯线性回归
    'Poisson Regression': PoissonRegressor()  # 广义线性回归（泊松回归）
}

# 训练模型并进行预测
predictions = {}
metrics = {}
best_model_name = None
best_r2 = -np.inf

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions[name] = model.predict(X_test)
    r2 = r2_score(y_test, predictions[name])
    rmse = np.sqrt(mean_squared_error(y_test, predictions[name]))
    metrics[name] = (r2, rmse)

    # 保存最优模型
    if r2 > best_r2:
        best_r2 = r2
        best_model_name = name
        best_model = model

# 保存最优模型为 joblib 文件
best_model_path = f"best_model_{best_model_name}.joblib"
joblib.dump(best_model, best_model_path)
print(f"最优模型 {best_model_name} 已保存到 {best_model_path}")

# 可视化比较
plt.figure(figsize=(15, 7))

for i, (name, pred) in enumerate(predictions.items(), 1):
    plt.subplot(2, 3, i)
    plt.scatter(y_test, pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
    plt.title(name)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    # 添加指标到图表
    r2, rmse = metrics[name]
    plt.annotate(f'$R^2$: {r2:.2f}\nRMSE: {rmse:.2f}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12,
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))

plt.tight_layout()
plt.show()