import csv
import wfdb
import os
# 设置数据的基础路径
DATA = "data"
'''
这个文件用来将dat文件转换为csv格式
'''


def get_data(idx):
    # 读取数据
    path = os.path.join(DATA, idx)
    data_row = wfdb.rdrecord(path)
    data_ecg = data_row.p_signal
    leads = data_row.sig_name
    # 创建 CSV
    filename = f"{idx}.csv"
    outfile = open(filename, "w")
    out_csv = csv.writer(outfile)
    # 写入带有导联名称的 CSV 标题
    out_csv.writerow(leads)
    # 将心电图数据写入 CSV
    for row in data_ecg:
        out_csv.writerow(row)


if __name__== '__main__':
    idx = '102'
    get_data(idx)
