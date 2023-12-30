import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
import save_csv as sc
import numpy as np
import scipy.fftpack

# 样本长度
sample = 5000.0

# 采样频率和周期
Fs = 1000
T = 1.0/Fs

# 创建时间轴
x = np.linspace(0.0, sample*T, 5000)
# 创建频域轴
xf = np.linspace(0.0,1.0/(2.0*T), 2500)

ecg_data = pd.read_csv('output_flattened.csv')
ecg_signal1 = ecg_data.iloc[:, 0].values
# 计算信号的离散傅里叶变换结果
lead1_f = scipy.fftpack.fft(ecg_signal1)
print(lead1_f)
ecg_signal2 = nk.ecg_clean(ecg_signal1, sampling_rate=1000, method='pantompkins1985')
# 计算信号的离散傅里叶变换结果
lead2_f = scipy.fftpack.fft(ecg_signal2)
# 创建绘制子图
fig_td1 = plt.figure()
fig_td1.suptitle('Time domain signals')
fig_fd2 = plt.figure()
fig_fd2.suptitle('Frequency domain signals')
# 设置子图布局
fig_td1.subplots_adjust(hspace=0.5)  # 设置垂直方向上的子图间距
fig_fd2.subplots_adjust(hspace=0.5)
ax1 = fig_td1.add_subplot(211)
ax1.set_title('Before filtering')
ax2 = fig_td1.add_subplot(212)
ax2.set_title('After filtering')
ax3 = fig_fd2.add_subplot(211)
ax3.set_title('Before filtering')
ax4 = fig_fd2.add_subplot(212)
ax4.set_title('After filtering')

# 绘制原始信号
ax1.plot(x, ecg_signal1[:5000], color='r', linewidth=0.7)
ax1.set_ylim([-0.25, 0.7])  # 设置y轴的范围
ax3.plot(xf, 2.0 / sample * np.abs(lead1_f[:2500]), color='r', linewidth=0.7, label='raw')
ax3.set_ylim([0, 1.0])
ax3.set_xlim([0, 500])

# 绘制滤波后的输出
ax4.plot(xf, 2.0 / sample * np.abs(lead2_f[:2500]), color='g', linewidth=0.7)
ax4.set_ylim([0, 1.0])  # 设置y轴的范围
ax4.set_xlim([0, 500])
# 绘制滤波后的时域信号
ax2.plot(x, ecg_signal2[:5000], color='g', linewidth=0.7)
ax2.set_ylim([-0.25, 0.7])  # 设置y轴的范围
print(ecg_signal1)
print(lead1_f)
print(ecg_signal2)
print(lead2_f)
plt.show()
