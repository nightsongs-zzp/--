import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# 解决中文显示问题的核心代码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体（支持中文）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题


# ============ 1. 无空气阻力的抛体运动 ============

def projectile_motion_no_drag(v0, theta, g=9.8):
    """计算无阻力抛体运动轨迹"""
    theta_rad = np.deg2rad(theta)
    
    # 计算初速度分量
    v0x = v0 * np.cos(theta_rad)
    v0y = v0 * np.sin(theta_rad)
    
    # 计算飞行时间（当y=0时）
    T = 2 * v0y / g
    
    # 生成时间数组
    t = np.linspace(0, T, 100)
    
    # 计算轨迹
    x = v0x * t
    y = v0y * t - 0.5 * g * t**2
    
    # 确保y值非负
    y = np.maximum(y, 0)
    
    return x, y, T

# 参数设置
v0 = 20.0  # 初速度 m/s
g = 9.8    # 重力加速度 m/s²
angles = [15, 30, 45, 60, 75]  # 发射角度

# 绘制不同角度的轨迹
plt.figure(figsize=(10, 6))
max_range = 0
max_angle = 0

for theta in angles:
    x, y, T = projectile_motion_no_drag(v0, theta, g)
    range_val = x[-1]  # 射程
    
    # 跟踪最大射程
    if range_val > max_range:
        max_range = range_val
        max_angle = theta
    
    plt.plot(x, y, label=f'θ={theta}°, 射程={range_val:.2f}m')

plt.title('无空气阻力抛体运动 - 不同发射角度轨迹', fontsize=14, fontweight='bold')
plt.xlabel('水平距离 (m)', fontsize=12)
plt.ylabel('高度 (m)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.annotate(f'最大射程: {max_range:.2f}m (θ={max_angle}°)', 
             xy=(0.05, 0.95), xycoords='axes fraction',
             fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
plt.tight_layout()
plt.show()

# 验证45°时射程最大
print("=== 无空气阻力情况 ===")
print(f"理论最大射程角度: 45°")
print(f"模拟得到最大射程角度: {max_angle}°")
print(f"45°时射程: {projectile_motion_no_drag(v0, 45, g)[0][-1]:.2f}m")

# ============ 2. 考虑空气阻力 ============

def drag_projectile(t, state, b_over_m, g):
    """考虑空气阻力的抛体运动微分方程"""
    x, y, vx, vy = state
    dxdt = vx
    dydt = vy
    dvxdt = -b_over_m * vx
    dvydt = -g - b_over_m * vy
    return [dxdt, dydt, dvxdt, dvydt]

def solve_drag_projectile(v0, theta, b_over_m, g=9.8):
    """数值求解有阻力的抛体运动"""
    theta_rad = np.deg2rad(theta)
    
    # 初始条件
    x0, y0 = 0, 0
    vx0 = v0 * np.cos(theta_rad)
    vy0 = v0 * np.sin(theta_rad)
    initial_state = [x0, y0, vx0, vy0]
    
    # 事件：当物体落地时停止（y=0且下降）
    def hit_ground(t, state, b_over_m, g):
        return state[1]
    hit_ground.terminal = True
    hit_ground.direction = -1
    
    # 求解时间范围
    t_span = (0, 10)  # 最大10秒
    t_eval = np.linspace(0, 10, 1000)
    
    # 使用Runge-Kutta方法求解
    sol = solve_ivp(drag_projectile, t_span, initial_state, 
                    args=(b_over_m, g), t_eval=t_eval,
                    events=hit_ground, method='RK45', rtol=1e-8)
    
    return sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3]

# 参数设置
theta = 45
b_over_m_values = [0, 0.1, 0.3, 0.5]

# 绘制不同阻力系数下的轨迹
plt.figure(figsize=(10, 6))

for b_over_m in b_over_m_values:
    t, x, y, vx, vy = solve_drag_projectile(v0, theta, b_over_m, g)
    
    # 只取y>=0的部分
    mask = y >= 0
    x_valid = x[mask]
    y_valid = y[mask]
    
    label = f'b/m={b_over_m}'
    if b_over_m == 0:
        label += ' (无阻力)'
    
    plt.plot(x_valid, y_valid, label=label, linewidth=2)

plt.title(f'考虑空气阻力的抛体运动 (θ={theta}°)', fontsize=14, fontweight='bold')
plt.xlabel('水平距离 (m)', fontsize=12)
plt.ylabel('高度 (m)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.tight_layout()
plt.show()

# ============ 分析有阻力时的最佳发射角 ============

def find_max_range_with_drag(b_over_m, angles_to_test=np.linspace(10, 80, 15)):
    """寻找有阻力时的最佳发射角"""
    ranges = []
    
    for theta_test in angles_to_test:
        t, x, y, vx, vy = solve_drag_projectile(v0, theta_test, b_over_m, g)
        mask = y >= 0
        if len(x[mask]) > 0:
            range_val = x[mask][-1]  # 射程
            ranges.append(range_val)
        else:
            ranges.append(0)
    
    # 找到最大射程对应的角度
    max_range_idx = np.argmax(ranges)
    best_theta = angles_to_test[max_range_idx]
    max_range_val = ranges[max_range_idx]
    
    return angles_to_test, ranges, best_theta, max_range_val

# 对于每个阻力系数，寻找最佳角度
plt.figure(figsize=(10, 6))

# 存储有阻力时的结果
drag_results = {}

for b_over_m in b_over_m_values[1:]:  # 跳过0（无阻力）
    angles_to_test, ranges, best_theta, max_range_val = find_max_range_with_drag(b_over_m)
    drag_results[b_over_m] = {'best_theta': best_theta, 'max_range': max_range_val}
    
    plt.plot(angles_to_test, ranges, 'o-', label=f'b/m={b_over_m}, 最佳角度={best_theta:.1f}°')

# 无阻力情况的理论曲线
angles_theory = np.linspace(10, 80, 71)
ranges_no_drag = [v0**2 * np.sin(2*np.deg2rad(theta))/g for theta in angles_theory]
plt.plot(angles_theory, ranges_no_drag, 'k--', label='无阻力理论值 (45°最佳)')

plt.title('不同阻力系数下的射程与发射角关系', fontsize=14, fontweight='bold')
plt.xlabel('发射角度 (°)', fontsize=12)
plt.ylabel('射程 (m)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# ============ 3. 能量分析 ============

def calculate_energy(x, y, vx, vy, m=1, g=9.8):
    """计算机械能"""
    kinetic = 0.5 * m * (vx**2 + vy**2)
    potential = m * g * y
    return kinetic + potential

# 无阻力情况能量分析
print("\n=== 无阻力能量分析 ===")
x, y, T = projectile_motion_no_drag(v0, 45, g)
# 为无阻力情况计算速度和能量
t_no_drag = np.linspace(0, T, 100)
vx_no_drag = v0 * np.cos(np.deg2rad(45))
vy_no_drag = v0 * np.sin(np.deg2rad(45)) - g * t_no_drag
energy_no_drag = calculate_energy(x, y, vx_no_drag, vy_no_drag)

print(f"初始能量: {energy_no_drag[0]:.2f} J")
print(f"最终能量: {energy_no_drag[-1]:.2f} J")
print(f"能量变化: {energy_no_drag[-1] - energy_no_drag[0]:.2e} J")
print(f"能量守恒性: {np.std(energy_no_drag):.2e} J (标准差)")

# 有阻力情况能量分析
print("\n=== 有阻力能量分析 (b/m=0.3) ===")
t_drag, x_drag, y_drag, vx_drag, vy_drag = solve_drag_projectile(v0, 45, 0.3, g)
mask = y_drag >= 0
energy_drag = calculate_energy(x_drag[mask], y_drag[mask], vx_drag[mask], vy_drag[mask])

print(f"初始能量: {energy_drag[0]:.2f} J")
print(f"最终能量: {energy_drag[-1]:.2f} J")
print(f"能量损失: {energy_drag[0] - energy_drag[-1]:.2f} J")
print(f"能量损失百分比: {(energy_drag[0] - energy_drag[-1])/energy_drag[0]*100:.1f}%")

# 绘制能量变化图
plt.figure(figsize=(12, 8))

# 无阻力能量
plt.subplot(2, 2, 1)
plt.plot(t_no_drag, energy_no_drag)
plt.title('无阻力情况 - 机械能变化', fontsize=12)
plt.xlabel('时间 (s)')
plt.ylabel('机械能 (J)')
plt.grid(True, alpha=0.3)
plt.axhline(y=energy_no_drag[0], color='r', linestyle='--', alpha=0.5, label='初始能量')
plt.legend()

# 有阻力能量
plt.subplot(2, 2, 2)
plt.plot(t_drag[mask], energy_drag)
plt.title('有阻力情况 (b/m=0.3) - 机械能变化', fontsize=12)
plt.xlabel('时间 (s)')
plt.ylabel('机械能 (J)')
plt.grid(True, alpha=0.3)
plt.axhline(y=energy_drag[0], color='r', linestyle='--', alpha=0.5, label='初始能量')
plt.legend()

# 轨迹对比
plt.subplot(2, 2, 3)
# 无阻力
x_no, y_no, _ = projectile_motion_no_drag(v0, 45, g)
plt.plot(x_no, y_no, 'b-', label='无阻力', linewidth=2)
# 有阻力
mask = y_drag >= 0
plt.plot(x_drag[mask], y_drag[mask], 'r-', label='有阻力 (b/m=0.3)', linewidth=2)
plt.title('轨迹对比 (θ=45°)', fontsize=12)
plt.xlabel('水平距离 (m)')
plt.ylabel('高度 (m)')
plt.grid(True, alpha=0.3)
plt.legend()

# 速度变化对比
plt.subplot(2, 2, 4)
speed_no_drag = np.sqrt(vx_no_drag**2 + vy_no_drag**2)
speed_drag = np.sqrt(vx_drag[mask]**2 + vy_drag[mask]**2)
plt.plot(t_no_drag, speed_no_drag, 'b-', label='无阻力', linewidth=2)
plt.plot(t_drag[mask], speed_drag, 'r-', label='有阻力 (b/m=0.3)', linewidth=2)
plt.title('速度大小变化对比', fontsize=12)
plt.xlabel('时间 (s)')
plt.ylabel('速度大小 (m/s)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# ============ 4. 简单动画 (选做) ============

def create_animation():
    """创建抛体运动动画"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 计算轨迹
    x_no, y_no, _ = projectile_motion_no_drag(v0, 45, g)
    t_drag, x_drag, y_drag, _, _ = solve_drag_projectile(v0, 45, 0.3, g)
    mask = y_drag >= 0
    x_drag, y_drag = x_drag[mask], y_drag[mask]
    
    # 设置坐标轴范围
    max_x = max(np.max(x_no), np.max(x_drag))
    max_y = max(np.max(y_no), np.max(y_drag))
    ax.set_xlim(0, max_x * 1.1)
    ax.set_ylim(0, max_y * 1.1)
    ax.set_xlabel('水平距离 (m)')
    ax.set_ylabel('高度 (m)')
    ax.set_title('抛体运动动画 (蓝色:无阻力, 红色:有阻力)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # 创建轨迹线和点
    line_no, = ax.plot([], [], 'b-', alpha=0.5, label='无阻力轨迹')
    line_drag, = ax.plot([], [], 'r-', alpha=0.5, label='有阻力轨迹')
    point_no, = ax.plot([], [], 'bo', markersize=8, label='无阻力物体')
    point_drag, = ax.plot([], [], 'ro', markersize=8, label='有阻力物体')
    ax.legend()
    
    # 动画初始化函数
    def init():
        line_no.set_data([], [])
        line_drag.set_data([], [])
        point_no.set_data([], [])
        point_drag.set_data([], [])
        return line_no, line_drag, point_no, point_drag
    
    # 动画更新函数
    def update(frame):
        # 每5帧更新一次
        idx = frame * 5
        
        # 无阻力动画
        if idx < len(x_no):
            line_no.set_data(x_no[:idx], y_no[:idx])
            point_no.set_data([x_no[idx]], [y_no[idx]])
        else:
            line_no.set_data(x_no, y_no)
            point_no.set_data([x_no[-1]], [y_no[-1]])
        
        # 有阻力动画
        if idx < len(x_drag):
            line_drag.set_data(x_drag[:idx], y_drag[:idx])
            point_drag.set_data([x_drag[idx]], [y_drag[idx]])
        else:
            line_drag.set_data(x_drag, y_drag)
            point_drag.set_data([x_drag[-1]], [y_drag[-1]])
        
        return line_no, line_drag, point_no, point_drag
    
    # 创建动画
    frames = max(len(x_no), len(x_drag)) // 5
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, 
                       interval=50, blit=True)
    
    plt.tight_layout()
    plt.show()
    
    return ani

# 运行动画（取消注释以运行）
ani = create_animation()

# ============ 结果分析与总结 ============

print("\n" + "="*50)
print("物理分析与总结")
print("="*50)

print("\n1. 有无空气阻力的物理差异：")
print("   a) 轨迹形状：无阻力时轨迹为对称抛物线；有阻力时轨迹不对称，下降段更陡")
print("   b) 射程：空气阻力显著减小射程")
print("   c) 最大高度：空气阻力减小最大高度")
print("   d) 飞行时间：空气阻力缩短飞行时间")
print("   e) 能量：无阻力时机械能守恒；有阻力时机械能不守恒，能量逐渐耗散")

print("\n2. 最佳发射角变化的原因：")
print("   无阻力时，理论最佳发射角为45°，此时水平速度和竖直速度达到最优平衡")
print("   有阻力时，最佳发射角小于45°。原因如下：")
print("   a) 阻力与速度平方成正比（近似），水平速度越大，阻力越大")
print("   b) 减小发射角可以减少水平速度分量，从而减小阻力影响")
print("   c) 需要更多垂直分量来延长飞行时间，补偿水平方向的阻力损失")

print("\n3. 数值结果总结：")

# 获取有阻力时的结果
b_over_m_03 = 0.3
best_theta_drag = drag_results[b_over_m_03]['best_theta']
max_range_drag = drag_results[b_over_m_03]['max_range']

print(f"   无阻力最大射程：{max_range:.2f}m (θ={max_angle}°)")
print(f"   有阻力(b/m={b_over_m_03})时最大射程：{max_range_drag:.2f}m (θ={best_theta_drag:.1f}°)")
print(f"   有阻力时射程减少：{(max_range - max_range_drag):.2f}m ({((max_range - max_range_drag)/max_range*100):.1f}%)")

# 输出结论
print("\n" + "="*50)
print("主要结论")
print("="*50)
print("1. 无空气阻力时，45°发射角确实产生最大射程")
print("2. 空气阻力使轨迹不对称，减小射程、高度和飞行时间")
print("3. 随着阻力增加，最佳发射角从45°逐渐减小")
print("4. 机械能在无阻力时守恒，在有阻力时逐渐耗散")
print("5. 实际应用中需考虑空气阻力，最佳发射角通常小于45°")