import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# 解决中文显示问题的核心代码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体（支持中文）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# 定义被积函数
def integrand(x):
    return np.exp(-x**2)

# 精确值（通过SciPy计算）
exact_integral, _ = integrate.quad(integrand, 0, 1)
print(f"精确积分值: {exact_integral:.10f}")

# 蒙特卡洛积分实现
def monte_carlo_integral(N, a=0, b=1):
    """使用蒙特卡洛方法计算定积分"""
    # 生成均匀随机点
    x_random = np.random.uniform(a, b, N)
    
    # 计算函数值
    f_values = integrand(x_random)
    
    # 计算积分估计
    integral_estimate = (b - a) * np.mean(f_values)
    
    return integral_estimate

# 测试不同N值
N_values = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
mc_errors = []
mc_results = []

print("\n蒙特卡洛积分结果:")
print("N\t\t近似值\t\t误差\t\t相对误差")
for N in N_values:
    result = monte_carlo_integral(N)
    error = abs(result - exact_integral)
    mc_results.append(result)
    mc_errors.append(error)
    print(f"{N:6d}\t{result:.8f}\t{error:.2e}\t{error/exact_integral:.2e}")

# 绘制误差随N变化的图
plt.figure(figsize=(12, 5))

# 左图：误差随N变化
plt.subplot(1, 2, 1)
plt.loglog(N_values, mc_errors, 'bo-', linewidth=2, markersize=6, label='蒙特卡洛误差')
plt.loglog(N_values, [1/np.sqrt(N) for N in N_values], 'r--', linewidth=2, label='1/√N 参考线')
plt.xlabel('采样点数 N (对数坐标)', fontsize=12)
plt.ylabel('绝对误差 (对数坐标)', fontsize=12)
plt.title('蒙特卡洛积分误差分析', fontsize=14)
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend(fontsize=12)

# 右图：与确定性方法比较
plt.subplot(1, 2, 2)
n_det = [4, 8, 16, 32, 64, 128, 256]
det_errors = []

# 使用梯形法作为确定性方法比较
for n in n_det:
    x = np.linspace(0, 1, n+1)
    y = integrand(x)
    h = 1.0 / n
    trap_integral = h * (0.5*y[0] + 0.5*y[-1] + np.sum(y[1:-1]))
    det_errors.append(abs(trap_integral - exact_integral))

# 对应的N值（为了与蒙特卡洛比较）
det_N = n_det  # 梯形法需要的函数计算次数为n+1

plt.loglog(det_N, det_errors, 'g^-', linewidth=2, markersize=6, label='梯形法误差')
plt.loglog(N_values, mc_errors, 'bo-', linewidth=2, markersize=6, label='蒙特卡洛误差')
plt.xlabel('函数计算次数 (对数坐标)', fontsize=12)
plt.ylabel('绝对误差 (对数坐标)', fontsize=12)
plt.title('蒙特卡洛与梯形法比较', fontsize=14)
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend(fontsize=12)

plt.tight_layout()
plt.show()

# 分析收敛速率
print("\n蒙特卡洛收敛速率分析:")
for i in range(1, len(N_values)):
    error_ratio = mc_errors[i-1] / mc_errors[i]
    N_ratio = np.sqrt(N_values[i] / N_values[i-1])
    print(f"N从{N_values[i-1]}到{N_values[i]}: "
          f"误差比={error_ratio:.3f}, √N比={N_ratio:.3f}, "
          f"比值接近1/√N: {abs(error_ratio - N_ratio)/N_ratio:.3f}")

# 方法优缺点总结
print("\n" + "="*60)
print("方法比较与优缺点总结:")
print("="*60)
print("\n1. 确定性方法（梯形法、Simpson法）:")
print("   优点:")
print("   - 收敛速度快（梯形法O(h²)，Simpson法O(h⁴))")
print("   - 结果确定，可重复")
print("   - 对一维问题非常高效")
print("   缺点:")
print("   - 维数灾难：高维时计算量指数增长")
print("   - 对不规则区域处理困难")

print("\n2. 蒙特卡洛方法:")
print("   优点:")
print("   - 维数无关：误差与1/√N成正比，与维度无关")
print("   - 对复杂区域和积分容易实现")
print("   - 天然适合并行计算")
print("   缺点:")
print("   - 收敛速度慢（1/√N）")
print("   - 结果具有随机性，需要多次平均")
print("   - 对于低维问题不如确定性方法高效")

print("\n3. 适用场景:")
print("   - 低维规则区域：使用确定性方法")
print("   - 高维问题（>3维）：优先考虑蒙特卡洛方法")
print("   - 复杂几何区域：蒙特卡洛方法更有优势")
print("   - 需要快速近似：蒙特卡洛方法实现简单")