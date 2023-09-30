import radar_signal
import os
import matplotlib.pyplot as plt
import numpy as np
import math

fp_dataset = 'F:/我的坚果云/radar/dataset/'
sample_frequency = 1250
detection_window = int(3.0*sample_frequency)
fft_window = 64
fft_overlay = 32


def generate_pbc(sig, fs, win, overlap, f_lower, f_upper):
    if len(sig) == 0:
        return None
    is_complex = False
    if isinstance(sig[0], complex):
        is_complex = True
    print(is_complex)
    f, t, zxx = radar_signal.perform_stft(sig, fs, win, overlap)
    spec = np.array(zxx)
    idx_f_lower = int(win/2 + math.ceil(f_lower/(fs/win)))
    idx_f_upper = int(win/2 + math.floor(f_upper/(fs/win)))
    spec_in_range = spec[idx_f_lower:idx_f_upper] +
    print(f[idx_f_lower], f[idx_f_upper])
    print(win//2)
    print(f[win-idx_f_lower], f[win-idx_f_upper])


def getDensity(data):
    thread=20
    threadm=300
    Fs=1250
    L=data.__len__()
    X=data
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    sp=plt.specgram(X,NFFT=80,Fs=1250,noverlap=40)
    spec=np.array(sp[0])

    rbvsdp=spec[20:38]+spec[42:60]
    rbvsdp=np.array(rbvsdp).transpose(1,0)
    pbc=np.zeros((rbvsdp.shape[0]))
    for idx in range(0,rbvsdp.shape[0]):
        pbc[idx]=np.sum(rbvsdp[idx])

    pbc=np.log10(pbc+1)
    u = pbc.mean()  # 计算均值
    std = pbc.std()  # 计算标准差
    res1,res2=stats.kstest(pbc, 'norm', (u, std))


    return res1,res2


if __name__ == '__main__':
    for subject in os.listdir(fp_dataset):  # 遍历每一个受试者
        fp1 = fp_dataset+subject
        if not os.path.isdir(fp1):
            # print(fp1 + " is not a directory")
            continue
        for action in os.listdir(fp1):  # 遍历每一个动作
            fp2 = fp1 + '/' + action
            if not os.path.isdir(fp2):
                # print(fp2 + " is not a directory")
                continue
            if (not os.path.exists(fp2 + '/Radar1I.txt')
                    or not os.path.exists(fp2 + '/Radar1Q.txt')
                    or not os.path.exists(fp2 + '/Radar2I.txt')
                    or not os.path.exists(fp2 + '/Radar2Q.txt')
                    or not os.path.exists(fp2 + '/Tag_Start_End.txt')):
                # print(fp2+" is incomplete")
                continue
            # ############################################# 读取数据 ####################################################### #
            # 读取上方雷达原始数据
            f = open(fp2 + '/Radar1I.txt', "r")
            abovei = list(map(int, f.read().strip(',').split(',')))
            f.close()

            f = open(fp2 + '/Radar1Q.txt', "r")  #
            aboveq = list(map(int, f.read().strip(',').split(',')))
            f.close()
            # 校正上方雷达数据
            aboveq = radar_signal.calibrate(abovei, aboveq, 1.294434286, -0.213409)

            # 滤波，组成复信号
            signal_above = radar_signal.combine(radar_signal.filtrate(abovei), radar_signal.filtrate(aboveq))

            # 读取侧方雷达原始数据
            f = open(fp2 + '/Radar2I.txt', "r")  #
            sidei = list(map(int, f.read().strip(',').split(',')))
            f.close()

            f = open(fp2 + '/Radar2Q.txt', "r")  #
            sideq = list(map(int, f.read().strip(',').split(',')))
            f.close()

            # 校正侧方雷达数据
            sideq = radar_signal.calibrate(sidei, sideq, 1.201770976, -0.217531829)
            # 陷波滤波，组成复信号
            signal_side = radar_signal.combine(radar_signal.filtrate(sidei), radar_signal.filtrate(sideq))

            f = open(fp2 + '/Tag_Start_End.txt', "r")  # 设置文件对象
            lines = f.read().strip().strip(',').strip('\n').split('\n')
            tag = [[int(num) for num in line.split(',')] for line in lines]
            f.close()  # 关闭文件

            generate_pbc(sidei[tag[0][0]:tag[0][0]+4320], sample_frequency, 128, 120, 2, 300)