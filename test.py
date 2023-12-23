import neurokit2 as nk
import matplotlib.pyplot as plt
'''
这段代码旨在测试功能
'''

# 这个数据集包含心电图（ECG）、呼吸信号（RSP），
# 以及皮肤电活动（EDA）等信号，采样率为 100 Hz
data = nk.data("bio_eventrelated_100hz")

# 对生物信号数据进行预处理。具体而言，
# 对心电图（ECG）、呼吸信号（RSP），以及皮肤电活动（EDA）
# 进行了滤波、寻找峰值等处理。处理后的数据和相关信息存储在
# processed_data 和 info 变量中,以ecg为例
processed_data, info = nk.bio_process(ecg=data["ECG"], sampling_rate=100)

# 使用处理过的数据计算相关的特征。包括心率、
# 呼吸率、皮肤电活动的振幅等。结果存储在 results 变量中。
results = nk.bio_analyze(processed_data, sampling_rate=100)

# 下面展示结果
# Plot ECG signal
xlim = 500

plt.figure(figsize=(8, 6))
plt.subplot(1, 1, 1)
plt.plot(data["ECG"],color='red')
plt.ylim(-1.5, 1.5)
# 设置 x 轴范围为 0 到 2000
plt.xlim(0, xlim)
plt.title('ECG Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Plot processed ECG signal
plt.subplot(1, 1, 1)
plt.plot(processed_data["ECG_Clean"])

plt.ylim(-1.5, 1.5)
# 设置 x 轴范围为 0 到 2000
plt.xlim(0, xlim)
plt.title('ECG_Clean')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Plot processed ECG signal
plt.subplot(1, 1, 1)
# 获取 R 峰的位置
r_peak_indices = [i for i, value in enumerate(processed_data["ECG_R_Peaks"]) if value == 1]
# 绘制散点图
plt.scatter(r_peak_indices, [1] * len(r_peak_indices), marker='o', color='red')
plt.ylim(-1.5, 1.5)
# 设置 x 轴范围为 0 到 2000
plt.xlim(0, xlim)
plt.title('R peaks')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
# Show the plots
plt.tight_layout()
plt.show()

