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
# processed_data 和 info 变量中
processed_data, info = nk.bio_process(ecg=data["ECG"], sampling_rate=100)

# 使用处理过的数据计算相关的特征。这可能包括心率、
# 呼吸率、皮肤电活动的振幅等。结果存储在 results 变量中。
results = nk.bio_analyze(processed_data, sampling_rate=100)

# 下面展示结果
# Plot ECG signal
plt.figure(figsize=(12, 4))
plt.subplot(2, 1, 1)
plt.plot(data["ECG"])
plt.title('ECG Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
# Plot processed ECG signal
plt.subplot(2, 1, 2)
plt.plot(processed_data["ECG_Clean"])
plt.title('Processed ECG Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Show the plots
plt.tight_layout()
plt.show()

