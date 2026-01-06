import numpy as np
import matplotlib.pyplot as plt

# 定义被积函数
def f(x):
    return np.sin(x)

# 精确积分值
exact_value = 2.0

# 梯形法实现
def trapezoidal_rule(a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    integral = h * (0.5*y[0] + 0.5*y[-1] + np.sum(y[1:-1]))
    return integral

# Simpson法实现
def simpson_rule(a, b, n):
    if n % 2 != 0:
        n += 1  # 确保n为偶数
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)
    integral = h/3 * (y[0] + y[-1] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]))
    return integral

# 测试不同n值
n_values = [4, 8, 16, 32, 64]
trap_errors = []
simpson_errors = []
trap_values = []
simpson_values = []

for n in n_values:
    trap_val = trapezoidal_rule(0, np.pi, n)
    simpson_val = simpson_rule(0, np.pi, n)
    
    trap_values.append(trap_val)
    simpson_values.append(simpson_val)
    
    trap_errors.append(abs(trap_val - exact_value))
    simpson_errors.append(abs(simpson_val - exact_value))
    
    print(f"n={n:2d}: 梯形法={trap_val:.8f} (误差={trap_errors[-1]:.2e}), "
          f"Simpson法={simpson_val:.8f} (误差={simpson_errors[-1]:.2e})")

# 绘制误差随n变化的双对数图
plt.figure(figsize=(10, 6))
h_values = [np.pi / n for n in n_values]

# 梯形法误差
plt.loglog(h_values, trap_errors, 'bo-', linewidth=2, markersize=8, label='梯形法误差')
# Simpson法误差
plt.loglog(h_values, simpson_errors, 'ro-', linewidth=2, markersize=8, label='Simpson法误差')

# 绘制参考线：O(h^2) 和 O(h^4)
ref_h2 = [0.1 * h**2 for h in h_values]
ref_h4 = [0.1 * h**4 for h in h_values]
plt.loglog(h_values, ref_h2, 'b--', linewidth=1, label='O(h²) 参考线')
plt.loglog(h_values, ref_h4, 'r--', linewidth=1, label='O(h⁴) 参考线')

plt.xlabel('步长 h (对数坐标)', fontsize=12)
plt.ylabel('绝对误差 (对数坐标)', fontsize=12)
plt.title('数值积分误差分析: ∫₀^π sin(x)dx = 2', fontsize=14)
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# 计算收敛阶
print("\n收敛阶分析:")
for i in range(1, len(n_values)):
    trap_order = np.log(trap_errors[i-1]/trap_errors[i]) / np.log(2)
    simpson_order = np.log(simpson_errors[i-1]/simpson_errors[i]) / np.log(2)
    print(f"n从{n_values[i-1]}到{n_values[i]}: "
          f"梯形法收敛阶={trap_order:.3f}, "
          f"Simpson法收敛阶={simpson_order:.3f}")