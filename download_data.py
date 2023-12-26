import glob
import numpy as np
import os
import wfdb
import pickle
# 设置数据的基础路径
DATA = "data"


#  用于读取 .dat 文件中的波形数据并以 NumPy 数组的形式返回
def extract_wave(idx, len):
    """
    读取.dat文件并返回NumPy数组。假定有2个通道。返回的数组是n x 3，其中n是样本数。
    第一列是样本编号，接下来两列是第一和第二通道的数据。
    """
    record_path = os.path.join(DATA, idx)
    output, metadata = wfdb.rdsamp(record_path)
    data = np.frombuffer(output.tobytes(), dtype=np.int32)
    data = data[500:len]
    data = data.reshape((-1, 2))
    data = data.astype(np.float64) / (2 ** 32 - 1)
    return data, metadata


def save(example,idx):
    with open(os.path.join(DATA,"{}.pkl".format(idx)),'wb')as fid:
        pickle.dump(example[1], fid)


if __name__ == '__main__':
    files = glob.glob(os.path.join(DATA, "*.dat"))  # 使用 glob 获取数据路径下所有 .dat 文件的列表
    # 通过循环，获取每个文件的基本名称，即去除路径和文件扩展名的部分
    idxs = [os.path.basename(f).split(".")[0] for f in files]
    for idx in idxs:
        example = extract_wave(idx)
        save(example,idx)
        print("Example {} has extracted ".format(idx))
