import numpy as np
import matplotlib.pyplot as plt

# 解决中文显示问题的核心代码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体（支持中文）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# 高斯函数
def gaussian(x):
    return np.exp(-x**2)

# 精确值
exact_gaussian = np.sqrt(np.pi)

# 方法1: 截断法
def truncated_gaussian(L, n=1000):
    """使用梯形法计算截断后的高斯积分"""
    x = np.linspace(-L, L, n+1)
    y = gaussian(x)
    h = 2*L / n
    integral = h * (0.5*y[0] + 0.5*y[-1] + np.sum(y[1:-1]))
    return integral

# 方法2: 变量变换法
def transformed_gaussian(n=1000):
    """使用变换 t = x/√(1+x^2) 将无限区间映射到[-1,1]"""
    t = np.linspace(-1, 1, n+1)
    
    # 变换: t = x/√(1+x^2) ⇒ x = t/√(1-t^2)
    # dx/dt = 1/(1-t^2)^(3/2)
    x = t / np.sqrt(1 - t**2)
    dx_dt = 1 / (1 - t**2)**(1.5)
    
    # 被积函数: f(x) * dx/dt
    integrand = gaussian(x) * dx_dt
    
    # 使用Simpson法积分
    h = 2.0 / n
    integral = h/3 * (integrand[0] + integrand[-1] + 
                      4*np.sum(integrand[1:-1:2]) + 
                      2*np.sum(integrand[2:-2:2]))
    return integral

# 分析不同L值对截断法精度的影响
L_values = np.linspace(1, 10, 20)
truncated_errors = []

print("截断法分析:")
print("L值\t近似值\t\t误差\t\t相对误差")
for L in L_values:
    approx = truncated_gaussian(L)
    error = abs(approx - exact_gaussian)
    rel_error = error / exact_gaussian
    truncated_errors.append(error)
    print(f"{L:.1f}\t{approx:.8f}\t{error:.2e}\t{rel_error:.2e}")

# 绘制截断误差随L变化
plt.figure(figsize=(10, 6))
plt.plot(L_values, truncated_errors, 'bo-', linewidth=2)
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.xlabel('截断区间半宽 L', fontsize=12)
plt.ylabel('绝对误差', fontsize=12)
plt.title('高斯积分截断法误差分析: ∫₋∞⁺∞ e^{-x²}dx = √π', fontsize=14)
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.tight_layout()
plt.show()

# 变量变换法计算
transformed_result = transformed_gaussian(n=2000)
transformed_error = abs(transformed_result - exact_gaussian)

print(f"\n变量变换法结果:")
print(f"近似值: {transformed_result:.12f}")
print(f"精确值: {exact_gaussian:.12f}")
print(f"绝对误差: {transformed_error:.2e}")
print(f"相对误差: {transformed_error/exact_gaussian:.2e}")

# 比较两种方法
print(f"\n方法比较:")
print(f"截断法(L=5): {truncated_gaussian(5):.12f} (误差={abs(truncated_gaussian(5)-exact_gaussian):.2e})")
print(f"截断法(L=10): {truncated_gaussian(10):.12f} (误差={abs(truncated_gaussian(10)-exact_gaussian):.2e})")
print(f"变量变换法: {transformed_result:.12f} (误差={transformed_error:.2e})")