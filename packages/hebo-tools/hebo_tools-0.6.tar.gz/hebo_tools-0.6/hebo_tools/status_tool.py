import numpy as np


def get_status(data, fs):
    data = np.array(data[-fs * 4:])
    count_4095 = data.count(4095)
    count_0 = data.count(0)
    if count_0 > 5 or count_4095 > 5:
        return 2

    # 用最新的4秒判断是否离床
    segf_old = np.array(data[-fs * 4:])
    segf_mean = np.mean(segf_old)  # 平均值
    segf_old = segf_old - segf_mean  # 原始值减去平均值
    segf_old = np.abs(segf_old)
    std = np.median(segf_old)  # 中位数

    if std <= 25 and (300 < segf_mean < 3800):
        return 0  # 无人
    else:
        return 1  # 有人
