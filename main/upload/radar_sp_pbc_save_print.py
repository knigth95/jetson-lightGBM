import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib
from skimage import exposure
import scipy.stats as stats
import time
import os
import seaborn as sns
import sys

matplotlib.use("Agg")

# 创建文件夹函数


def mkdir(path):
    # os.path.exists 函数判断文件夹是否存在
    folder = os.path.exists(path)

    # 判断是否存在文件夹如果不存在则创建为文件夹
    if not folder:
        # os.makedirs 传入一个path路径，生成一个递归的文件夹；如果文件夹存在，就会报错,因此创建文件夹之前，需要使用os.path.exists(path)函数判断文件夹是否存在；
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print('文件夹创建成功：', path)

    else:
        print('文件夹已经存在：', path)


nextMotion = ['curveleg/', 'gettingup/', 'left/', 'right/', 'wavehand/']
root = 'D:/Personal/test/dataset/dataset/clfan/'


for i in range(0, 5):
    # 如果未创建计数文件，创建并加入0
    if (os.path.exists(root+nextMotion[i]+'last.txt') == False):
        fo = open(root+nextMotion[i]+'last.txt', 'a')
        fo.write('0')
        fo.close()
    drawTime = time.localtime()
    if (os.path.exists(root+nextMotion[i]+str(drawTime.tm_year)+'.'+str(drawTime.tm_mon)+'.'+str(drawTime.tm_mday)+'/image') == False):
        mkdir(root+nextMotion[i]+str(drawTime.tm_year)+'.' +
              str(drawTime.tm_mon)+'.'+str(drawTime.tm_mday)+'/image')
        mkdir(root+nextMotion[i]+str(drawTime.tm_year)+'.' +
              str(drawTime.tm_mon)+'.'+str(drawTime.tm_mday)+'/test')

    np.set_printoptions(threshold=sys.maxsize)
    I1_s = np.genfromtxt(
        root+nextMotion[i]+'Radar1I.txt', delimiter=',', filling_values=np.nan)  # 读取文本文件中的雷达数据
    Q1_s = np.genfromtxt(
        root+nextMotion[i]+'Radar1Q.txt', delimiter=',', filling_values=np.nan)  # 读取文本文件中的雷达数据

    # 取出将要继续存图的位置，存入num（以避免程序中断丢失位置）
    fo = open(root+nextMotion[i]+'last.txt', 'r')
    num = 0
    for numTemp in fo.readlines():
        num = int(numTemp)
        break
    fo.close()

    fs = 1250
    width = 0.3
    start_t = 1  # 开始索引
    k_t = 3  # 持续时间（s）
    kl = start_t*fs + num*k_t*fs  # 将要继续存图的开始索引

    try:
        while (True):
            start = kl
            end = int(start+k_t*fs)
            radar_signal1I = I1_s[start:end]
            radar_signal1Q = Q1_s[start:end]
            # 设定相关参数
            nperseg = 80
            noverlap = nperseg // 2
            freqs, times, spectrogram1I = signal.spectrogram(
                radar_signal1I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')
            freqs, times, spectrogram1Q = signal.spectrogram(
                radar_signal1Q, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')

            show_spectrogram1I = np.flip(spectrogram1I, axis=0)
            show_spectrogram = np.concatenate(
                (show_spectrogram1I, spectrogram1Q), axis=0)

            threshold_low = 2
            threshold_high = 300

            # 计算出STFT中每列处于阈值范围内的数据的总幅值
            pbc = np.log(np.add(np.sum(spectrogram1I[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0), np.sum(
                spectrogram1Q[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0))+1)

            fo = open(root+nextMotion[i]+'last.txt', 'r')
            for numTemp in fo.readlines():
                num = int(numTemp)
                break
            fo.close()

            # 计算每个时间点的坐标值
            time_axis = np.arange(len(radar_signal1I)) / fs

            # 绘制时频图和PBC分部图
            fig, axs = plt.subplots(2, 1, figsize=(
                8, 6), gridspec_kw=dict(height_ratios=[3, 1]))
            plt.subplots_adjust(hspace=0.5)
            # 时频图
            im = axs[0].imshow(np.log(show_spectrogram), cmap='viridis', aspect='auto', extent=[
                               time_axis[0], time_axis[-1], freqs[0], freqs[-1]])
            axs[0].set_xlabel('Time / s')
            axs[0].set_yticks([])

            # pbc绘制
            sns.histplot(pbc, bins=50, stat='density', kde=False)
            plt.xlabel('PBC')
            plt.ylabel('Density')
            plt.title('PBC Density Distribution')

            # 计算并绘制适合于数据的核密度估计和扩展概率密度函数（PDF）
            kde = stats.gaussian_kde(pbc)
            xmin, xmax = plt.xlim()
            x_plot = np.linspace(xmin, xmax, 1000)
            y_plot = kde.pdf(x_plot)
            plt.plot(x_plot, y_plot, color='red')

            # 保存PBC能量图
            plt.savefig(root+nextMotion[i]+str(drawTime.tm_year)+'.'+str(
                drawTime.tm_mon)+'.'+str(drawTime.tm_mday)+'/image/'+str(int(num)+1)+'.png')

            # 保存下一位置索引，存入last.txt
            fo = open(root+nextMotion[i]+'last.txt', 'w')
            fo.truncate(0)
            fo.write(str(num+1))
            fo.close()

            kl = start+k_t*fs
            plt.close('all')
    except:
        np.set_printoptions(threshold=sys.maxsize)
        start = kl
        end = len(I1_s)-1
        radar_signal1Itemp = I1_s[start:end]
        radar_signal1Qtemp = Q1_s[start:end]
        
        # 设定相关参数
        nperseg = 80
        noverlap = nperseg // 2
        freqs, times, spectrogram1I = signal.spectrogram(
            radar_signal1I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')
        freqs, times, spectrogram1Q = signal.spectrogram(
            radar_signal1Q, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')

        show_spectrogram1I = np.flip(spectrogram1I, axis=0)
        show_spectrogram = np.concatenate(
            (show_spectrogram1I, spectrogram1Q), axis=0)

        threshold_low = 2
        threshold_high = 300

        # 计算出STFT中每列处于阈值范围内的数据的总幅值
        pbc = np.log(np.add(np.sum(spectrogram1I[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0), np.sum(
            spectrogram1Q[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0))+1)

        fo = open(root+nextMotion[i]+'last.txt', 'r')
        for numTemp in fo.readlines():
            num = int(numTemp)
            break
        fo.close()

        # 计算每个时间点的坐标值
        time_axis = np.arange(len(radar_signal1I)) / fs

        # 绘制时频图和PBC分部图
        fig, axs = plt.subplots(2, 1, figsize=(
            8, 6), gridspec_kw=dict(height_ratios=[3, 1]))
        plt.subplots_adjust(hspace=0.5)
        # 时频图
        im = axs[0].imshow(np.log(show_spectrogram), cmap='viridis', aspect='auto', extent=[
                           time_axis[0], time_axis[-1], freqs[0], freqs[-1]])
        axs[0].set_xlabel('Time / s')
        axs[0].set_yticks([])

        # pbc绘制
        sns.histplot(pbc, bins=50, stat='density', kde=False)
        plt.xlabel('PBC')
        plt.ylabel('Density')
        plt.title('PBC Density Distribution')

        # 计算并绘制适合于数据的核密度估计和扩展概率密度函数（PDF）
        kde = stats.gaussian_kde(pbc)
        xmin, xmax = plt.xlim()
        x_plot = np.linspace(xmin, xmax, 1000)
        y_plot = kde.pdf(x_plot)
        plt.plot(x_plot, y_plot, color='red')

        # 保存PBC能量图
        plt.savefig(root+nextMotion[i]+str(drawTime.tm_year)+'.'+str(
            drawTime.tm_mon)+'.'+str(drawTime.tm_mday)+'/image/'+str(int(num)+1)+'.png')

        # 保存下一位置索引，存入last.txt
        fo = open(root+nextMotion[i]+'last.txt', 'w')
        fo.truncate(0)
        fo.write(str(num+1))
        fo.close()
