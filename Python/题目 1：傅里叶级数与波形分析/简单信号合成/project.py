import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# 定义复合信号
def composite_signal(t):
    return (np.sin(2*np.pi*3*t) + 
            0.5*np.sin(2*np.pi*7*t) + 
            0.3*np.sin(2*np.pi*11*t))

# 生成时域信号
fs = 1000  # 采样频率
t = np.linspace(0, 2, 2*fs)  # 2秒时长
s = composite_signal(t)

# 时域波形图
plt.figure(figsize=(12, 8))

# 时域图
plt.subplot(2, 1, 1)
plt.plot(t, s, 'b-', linewidth=1)
plt.title('复合信号时域波形: s(t) = sin(2π·3t) + 0.5sin(2π·7t) + 0.3sin(2π·11t)')
plt.xlabel('时间 t (秒)')
plt.ylabel('振幅')
plt.grid(True)
plt.xlim(0, 2)

# FFT分析
n = len(t)
freqs = fftfreq(n, 1/fs)[:n//2]
fft_vals = fft(s)[:n//2]
magnitude = np.abs(fft_vals) / (n/2)  # 归一化幅度

# 频域图
plt.subplot(2, 1, 2)
plt.stem(freqs, magnitude, 'r', markerfmt='ro', basefmt=" ")
plt.title('复合信号频谱分析 (FFT)')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.grid(True)
plt.xlim(0, 15)  # 显示0-15Hz范围

# 标记预期频率
expected_freqs = [3, 7, 11]
for freq in expected_freqs:
    plt.axvline(x=freq, color='g', linestyle='--', alpha=0.5)
    plt.text(freq, max(magnitude)*0.9, f'{freq} Hz', 
             horizontalalignment='center')

plt.tight_layout()
plt.show()

# 验证频率成分
print("检测到的主要频率成分：")
for i in range(len(freqs)):
    if magnitude[i] > 0.1:  # 设置阈值
        print(f"频率: {freqs[i]:.1f} Hz, 幅度: {magnitude[i]:.3f}")