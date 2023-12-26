import pandas as pd
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
import scipy.signal as signal

# 读入数据
dataset = pd.read_csv ("100.csv")

# 创建两个导联的列表
lead1 = [e for e in dataset.MLII]
lead2 = [e for e in dataset.V5]

# 样本长度
sample = 5000.0

# 采样频率和周期
Fs = 1000
T = 1.0/Fs

# 创建时间轴
x = np.linspace(0.0, sample*T, 5000)

# 计算信号的离散傅里叶变换结果
lead1_f = scipy.fftpack.fft(lead1)
lead2_f = scipy.fftpack.fft(lead2)

# 创建频域轴
xf = np.linspace(0.0,1.0/(2.0*T), 2500)

# 创建绘制子图
fig_td = plt.figure()
fig_td.suptitle('Time domain signals')
fig_fd = plt.figure()
fig_fd.suptitle('Frequency domain signals')
# 设置子图布局
fig_td.subplots_adjust(hspace=0.5)  # 设置垂直方向上的子图间距
fig_fd.subplots_adjust(hspace=0.5)
ax1 = fig_td.add_subplot(211)
ax1.set_title('Before filtering')
ax2 = fig_td.add_subplot(212)
ax2.set_title('After filtering')
ax3 = fig_fd.add_subplot(211)
ax3.set_title('Before filtering')
ax4 = fig_fd.add_subplot(212)
ax4.set_title('After filtering')

# 绘制原始信号
ax1.plot(x,lead1[:5000], color='r', linewidth=0.7)
ax3.plot(xf, 2.0/sample * np.abs(lead1_f[:2500]), color='r', linewidth=0.7, label='raw')
ax3.set_ylim([0, 0.2])

# 设置低通滤波器(50hz)和带阻滤波器
band_filt = np.array([45, 55])
a, b = signal.butter(2, band_filt/(Fs/2), 'bandstop', analog=False)
c, d = signal.butter(4, 50/(Fs/2), 'low')
# 计算频率响应
w, h = signal.freqz(a, b, worN=8000)
ax3.plot(w, 20 * np.log10(abs(h)))
tempf = signal.filtfilt(a,b, lead1[:5000])
tempf = signal.filtfilt(c,d, tempf)
yff = scipy.fftpack.fft(tempf)


