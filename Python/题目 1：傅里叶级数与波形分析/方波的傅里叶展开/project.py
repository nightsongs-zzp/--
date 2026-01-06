import numpy as np
import matplotlib.pyplot as plt

# 定义方波函数
def square_wave(x):
    return np.where((x % (2*np.pi)) < np.pi, 1, -1)

# 计算傅里叶级数部分和
def fourier_square(x, N):
    result = np.zeros_like(x)
    for n in range(1, N+1):
        if n % 2 == 1:  # 仅奇数项
            result += (4/(np.pi*n)) * np.sin(n*x)
    return result

# 创建x轴数据
x = np.linspace(-2*np.pi, 4*np.pi, 1000)

# 绘制不同项数的逼近
N_values = [3, 5, 11, 51]
plt.figure(figsize=(12, 8))

for i, N in enumerate(N_values, 1):
    plt.subplot(2, 2, i)
    plt.plot(x, square_wave(x), 'k-', linewidth=2, label='Original')
    plt.plot(x, fourier_square(x, N), 'r-', linewidth=1.5, label=f'N={N}')
    plt.title(f'方波傅里叶逼近 (N={N})')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.ylim(-1.5, 1.5)

plt.tight_layout()
plt.show()