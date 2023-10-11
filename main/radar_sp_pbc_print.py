import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter  
import seaborn as sns
from scipy import stats

s_radar_signal1I =  np.genfromtxt('./radarData/dataset/lq0104/left/Radar1I.txt', delimiter=',', filling_values=np.nan) # 读取文本文件中的雷达数据
s_radar_signal1Q =  np.genfromtxt('./radarData/dataset/lq0104/left/Radar1Q.txt', delimiter=',', filling_values=np.nan) # 读取文本文件中的雷达数据
fs=1250
width=0.03
while True:
    start_t=eval(input('请输入开始时间：'))
    if start_t==-1:break
    times_show=eval(input('请输入持续时间：'))
    start_t=int(start_t*1250)
    num_samples = int(fs * times_show)
    radar_signal1I= s_radar_signal1I[start_t:start_t+num_samples]
    radar_signal1Q= s_radar_signal1Q[start_t:start_t+num_samples]

    # 设定相关参数
    nperseg = 80
    noverlap = nperseg // 2
    freqs, times, spectrogram1I = signal.spectrogram(radar_signal1I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')
    freqs, times, spectrogram1Q = signal.spectrogram(radar_signal1Q, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='linear')


    show_spectrogram1I= np.flip(spectrogram1I, axis=0)
    show_spectrogram= np.concatenate((show_spectrogram1I, spectrogram1Q), axis=0)

    threshold_low=2
    threshold_high=300

    # 计算出STFT中每列处于阈值范围内的数据的总幅值
    pbc = np.log(np.add( np.sum(spectrogram1I[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0) ,np.sum(spectrogram1Q[(freqs >= threshold_low) & (freqs <= threshold_high), :], axis=0))+1)
    
    # 计算每个时间点的坐标值
    time_axis = np.arange(len(radar_signal1I)) / fs

    # 绘制时频图和PBC分部图
    fig, axs = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw=dict(height_ratios=[3, 1]))
    plt.subplots_adjust(hspace=0.5)
    # 时频图
    im = axs[0].imshow(np.log(show_spectrogram), cmap='viridis', aspect='auto', extent=[time_axis[0], time_axis[-1], freqs[0], freqs[-1]])
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
    plt.savefig('./picture/'+str(start_t)+'.png')
    # 显示图像
    plt.show()





