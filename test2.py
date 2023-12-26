import matplotlib.pyplot as plt
import download_data as dd


def plot_wave(idx):
    """
    绘制指定 idx 的波形数据（假设每个样本有两个通道）。
    """
    # 读取数据
    data, metadata = dd.extract_wave(idx, 600)

    # 绘制波形
    plt.figure(figsize=(10, 30))
    # 设置y轴范围为-1到1
    plt.ylim(-1, 1)
    plt.plot(data)

    # 添加标签和标题
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("ECG Signal Waveform for {}".format(idx))

    # 显示图形
    plt.show()


def get_data(idx):
    # 读取数据
    data, metadata = dd.extract_wave(idx, 600)
    # 使用数组切片操作将两个通道拆分为两个数组
    channel_1 = data[:, 0]
    channel_2 = data[:, 1]

    # 输出拆分后的数组
    print("Channel 1:", channel_1)
    print("Channel 2:", channel_2)
    return channel_1


idx = "100"
get_data(idx)
plot_wave(idx)

