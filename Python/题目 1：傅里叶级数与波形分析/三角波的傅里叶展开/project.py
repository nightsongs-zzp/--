# 解决中文显示问题的核心代码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体（支持中文）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# 定义三角波函数
import numpy as np
import matplotlib.pyplot as plt
def triangle_wave(x):
    x_mod = np.mod(x + np.pi, 2*np.pi) - np.pi
    return np.abs(x_mod)

# 计算三角波的傅里叶级数部分和
def fourier_triangle(x, N):
    result = np.ones_like(x) * np.pi/2
    for n in range(1, N+1):
        if n % 2 == 1:  # 仅奇数项
            result -= (4/(np.pi*n**2)) * np.cos(n*x)
    return result

# 创建x轴数据
x = np.linspace(-3*np.pi, 3*np.pi, 1000)

# 绘制不同项数的逼近
N_values = [1, 3, 5, 10]
plt.figure(figsize=(12, 8))

for i, N in enumerate(N_values, 1):
    plt.subplot(2, 2, i)
    plt.plot(x, triangle_wave(x), 'k-', linewidth=2, label='Original')
    plt.plot(x, fourier_triangle(x, N), 'r-', linewidth=1.5, label=f'N={N}')
    plt.title(f'三角波傅里叶逼近 (N={N})')
    plt.xlabel('x')
    plt.ylabel('g(x)')
    plt.legend()
    plt.grid(True)
    plt.ylim(-0.5, np.pi+0.5)

plt.tight_layout()
plt.show()