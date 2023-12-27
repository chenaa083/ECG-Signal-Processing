import math
import pandas as pd
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
import scipy.signal as signal
import download_data as dd

# 读入数据
# 从CSV文件中读取前5000个数据点
file_number = 100
filename = "{}.csv".format(file_number)
dd.get_data('{}'.format(file_number))
dataset = pd.read_csv(filename, nrows=5000)
column_names = dataset.columns[0:2].tolist()
column_names = [name.strip("[]") for name in column_names]
column_name1, column_name2 = column_names
print("Column names of the first two columns: ",column_name1,column_name2)

# 创建两个导联的列表
lead1 = [e for e in dataset[column_names[0]]]
lead2 = [e for e in dataset[column_names[1]]]

# 样本长度
sample = 5000.0

# 采样频率和周期
Fs = 1000
T = 1.0/Fs

# 创建时间轴
x = np.linspace(0.0, sample*T, 5000)
# 创建频域轴
xf = np.linspace(0.0,1.0/(2.0*T), 2500)

# 计算信号的离散傅里叶变换结果
lead1_f = scipy.fftpack.fft(lead1)
lead2_f = scipy.fftpack.fft(lead2)

# 设置低通滤波器(50hz)和带阻滤波器(45,50),处理电源线干扰
a, b = signal.butter(4, 50/(Fs/2), 'low')
band_filt = np.array([45, 50])
c, d = signal.butter(2, band_filt/(Fs/2), 'bandstop', analog=False)

# 绘制频率响应曲线
w, h = signal.freqz(a, b, worN=8000)

# 通过滤波器
tempf = signal.filtfilt(a,b, lead1[:5000])
tempf = signal.filtfilt(c,d, tempf)
lead1_ff = scipy.fftpack.fft(tempf)

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

# 对滤波后的信号进行FFT
lead1_ff = scipy.fftpack.fft(y_filt)

# 计算心率
dataset['filt'] = y_filt

hrw = 1  # 单侧窗口大小，作为采样频率的比例
fs = 333  # 示例数据集以300Hz的频率录制

# 计算了'filt'列的滚动均值
mov_avg = dataset.filt.rolling(int(hrw * fs)).mean()
# 计算了移动平均值函数返回NaN的地方，并使用平均心率值(avg_hr)来填充这些NaN值
avg_hr = (np.mean(dataset.filt))
mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
mov_avg = [(0.5+x) for x in mov_avg]

# 对移动平均值的结果进行了20%的调整，为了防止次级心脏收缩对结果的影响
mov_avg = [x*1.0 for x in mov_avg]
dataset['filt_rollingmean'] = mov_avg

# 用于标记感兴趣的区域（Regions of Interest，ROI），识别信号中的峰值位置
window = []
peaklist = []
listpos = 0  # 用一个计数器在不同的数据列上移动
for datapoint in dataset.filt:
    rollingmean = dataset.filt_rollingmean[listpos]  # 获取局部均值

    if (datapoint < rollingmean) and (len(window) < 1):  # 如果没有检测到R复合活动 -> 什么也不做
        listpos += 1

    elif (datapoint > rollingmean):  # 如果信号超过局部均值，标记ROI
        window.append(datapoint)
        listpos += 1

    else:  # 如果信号下降到局部均值以下 -> 确定最高点
        maximum = max(window)
        beatposition = listpos - len(window) + (window.index(max(window)))  # 标记点在X轴上的位置
        peaklist.append(beatposition)  # 将检测到的峰值添加到列表
        window = []  # 清除标记的ROI
        listpos += 1

# 根据先前检测到的峰值位置在信号图上标记并绘制峰值
ybeat = [dataset.filt[x] for x in peaklist]  # 获取所有峰值的y值，用于绘图

# 用于计算心率并输出结果
RR_list = []
cnt = 0
while (cnt < (len(peaklist)-1)):
    RR_interval = (peaklist[cnt+1] - peaklist[cnt])  # 计算两个峰值之间的距离，以样本数表示
    ms_dist = ((RR_interval / fs) * 1000.0)  # 将样本距离转换为毫秒距离
    RR_list.append(ms_dist)  # 添加到列表中
    cnt += 1
bpm = 60000 / np.mean(RR_list)  # 计算心率（每分钟心跳数）

if __name__ == '__main__':
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
    ax1.plot(x,lead1[:5000], color='r', linewidth=0.7)
    ax3.plot(xf, 2.0/sample * np.abs(lead1_f[:2500]), color='r', linewidth=0.7, label='raw')
    ax3.set_ylim([0, 0.20])
    ax3.set_xlim([0, 200])

    # 绘制滤波后的输出
    ax4.plot(xf, 2.0/sample * np.abs(lead1_ff[:2500]), color='g', linewidth=0.7)
    ax4.set_ylim([0, 0.20])  # 设置y轴的范围
    ax4.set_xlim([0, 200])
    # 绘制滤波后的时域信号
    ax2.plot(x, y_filt, color='g', linewidth=0.7)
    ax2.set_ylim([-0.5, 1.0])  # 设置y轴的范围

    fig_hr = plt.figure()
    fig_hr.suptitle('Peak detector')
    ax5 = fig_hr.add_subplot(111)
    ax5.set_title("Detected peaks in signal")
    # ax6.set_xlim(0,2500)
    ax5.plot(dataset.filt, alpha=0.5, color='blue')  # 绘制半透明的心率信号
    ax5.plot(mov_avg, color='green')  # 绘制移动平均线
    ax5.scatter(peaklist, ybeat, color='red')  # 标记检测到的峰值

    # 创建Matplotlib图形
    plt.figure(figsize=(10, 6))
    # 绘制频率响应曲线
    plt.plot(w, 20 * np.log10(abs(h)), color='b', linewidth=2, label='Frequency Response')
    # 设置图形属性
    plt.title('Digital Filter Frequency Response')
    plt.xlabel('Frequency [radians / sample]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.legend()

    print("the dataset is:\n",dataset)
    print("\nAverage Heart Beat is: %.01f\n" % (bpm))  # 四舍五入为1位小数并打印
    print("Numbers of peaks in sample are {0}".format(len(peaklist)))

    plt.show()

