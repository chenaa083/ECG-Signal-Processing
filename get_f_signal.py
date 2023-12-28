import pandas as pd
import numpy as np
import scipy.signal as signal
import download_data as dd

# 从CSV文件中读取前5000个数据点
file_number = 100
filename = "{}.csv".format(file_number)
dd.get_data('{}'.format(file_number))
dataset = pd.read_csv(filename)
column_names = dataset.columns[0:2].tolist()
column_names = [name.strip("[]") for name in column_names]
column_name1, column_name2 = column_names

lead1 = [e for e in dataset[column_names[0]]]
# 采样频率和周期
Fs = 1000
T = 1.0/Fs

# 设置低通滤波器(50hz)和带阻滤波器(45,50),处理电源线干扰
a, b = signal.butter(4, 50/(Fs/2), 'low')
band_filt = np.array([45, 55])
c, d = signal.butter(2, band_filt/(Fs/2), 'bandstop', analog=False)
# 通过滤波器
tempf = signal.filtfilt(a,b, lead1[:5000])
tempf = signal.filtfilt(c,d, tempf)
# 计算Kaiser窗口系数，消除基线漂移干扰
# Fs 是采样率，nyq_rate 是Nyquist频率（Nyquist rate），表示采样率的一半。
nyq_rate = Fs / 2.0

# 过渡带宽度，指从通带到阻带的过渡区域的宽度。设置为Nyquist频率的5%。
width = 5.0 / nyq_rate

# 阻带中的期望衰减，以分贝（dB）为单位。设置为60 dB。
ripple_db = 60.0

# 计算FIR滤波器的阶数和Kaiser窗口的参数。
O, beta = signal.kaiserord(ripple_db, width)

# 滤波器的截止频率。在这里设置为4.0 Hz。
cutoff_hz = 4.0

# 使用它创建低通滤波器
# 使用 firwin 函数结合 Kaiser 窗口创建低通 FIR 滤波器
# O 是滤波器的阶数，cutoff_hz 是滤波器的截止频率，nyq_rate 是Nyquist频率，beta 是Kaiser窗口的参数
taps = signal.firwin(O, cutoff_hz/nyq_rate, window=('kaiser', beta), pass_zero=False)

# 使用 lfilter 函数将信号 tempf 通过 FIR 滤波器进行滤波
y_filt = signal.lfilter(taps, 1.0, tempf)