import csv
import matplotlib.pyplot as plt

# 读取 CSV 文件
csv_file_path = 'output.csv'
with open(csv_file_path, 'r') as csvfile:
    # 从 CSV 文件读取数据
    csv_reader = csv.reader(csvfile)
    # 假设数据在第一行
    data = next(csv_reader)

# 将字符串列表转换为浮点数
data = [float(x) for x in data]

# 生成 x 坐标，假设数据是等间隔的
x = range(1, len(data) + 1)

# 绘制折线图
plt.plot(x, data)
plt.xlabel('样本')
plt.ylabel('数值')
plt.title('CSV 数据折线图')
plt.show()
