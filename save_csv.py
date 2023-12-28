import csv
import get_f_signal as gfs
import numpy as np

# 数组 y_filt
y_filt = gfs.y_filt
print(y_filt)

# 指定输出 CSV 文件的路径
csv_file_path = 'output.csv'

# 写入 CSV 文件
with open(csv_file_path, 'w', newline='') as csvfile:
    # 直接写入一维数组
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(y_filt)

# 读取 CSV 文件并转换为一维数组
flattened_data = np.genfromtxt(csv_file_path, delimiter=',')

# 打印结果
print(flattened_data)

# 保存一维数组到新的 CSV 文件
new_file_path = 'output.csv'
np.savetxt(new_file_path, flattened_data, delimiter=',')
