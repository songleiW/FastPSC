import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 生成示例数据
x = p.array([[1, 2, 3, 4, 5],
              [2, 3, 4, 5, 6],
              [3, 4, 5, 6, 7]])
y = np.arange(1, 4, 1)  # 第二个自变量
X, Y = np.meshgrid(x, y)
Z = np.array([[1, 2, 3, 4, 5],
              [2, 3, 4, 5, 6],
              [3, 4, 5, 6, 7]])

# 创建3D图形对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制3D柱状图，并标注z值
for i in range(len(x)):
    for j in range(len(y)):
        ax.bar3d(x[i], y[j], 0, 0.8, 0.8, Z[j, i], shade=True)
        ax.text(x[i] + 0.4, y[j] + 0.4, Z[j, i], str(Z[j, i]), color='red')

# 设置图形参数
ax.set_xlabel('$q$')
ax.set_ylabel('$|\mathcal{D}|$')
ax.set_zlabel('$\epsilon_L$')
# 保存为PDF文件
plt.savefig('plot_example.pdf', format='pdf')

# 删除所有空白边界
# 手动调整边界
plt.subplots_adjust(left=-0.1, right=1, bottom=0, top=1)
# 显示图形
plt.show()
