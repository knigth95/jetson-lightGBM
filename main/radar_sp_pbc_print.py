
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from skimage import exposure
import scipy.stats as stats

I1_s=  np.genfromtxt('../dataset/clfan/left/Radar1I.txt', delimiter=',', filling_values=np.nan)# 读取文本文件中的雷达数据
Q1_s=  np.genfromtxt('../dataset/clfan/left/Radar1Q.txt', delimiter=',', filling_values=np.nan)# 读取文本文件中的雷达数据
fs=1250
width=0.3
while True:
    start_t=eval(input('请输入开始索引：'))
    
    if start_t==-1 :break
    start=int(start_t)
    k_t=eval(input('请输入持续时间：'))
    end=int(start_t+k_t*fs)
    I1=I1_s[start:end]
    Q1=Q1_s[start:end]
    #=估计雷达参数AI/AQ和φ(t)
    # 校准Q(t)
    DCI1 = np.mean(I1)
    DCQ1 = np.mean(Q1)
    AI1=np.max(np.abs(I1-DCI1))*2
    AQ1=np.max(np.abs(Q1-DCQ1))*2
    # 计算互相关
    corr1 = np.correlate(I1, Q1[::-1], mode='full')
    # 寻找最大值所在的位置
    max_idx1 = np.argmax(corr1)
    # 计算相移量
    shift1= len(Q1) - max_idx1 - 1
    # 计算相移
    sampling_freq1 = fs 
    phase_shift1 = shift1 / sampling_freq1

    QC1 =AI1/AQ1/np.cos(phase_shift1)*Q1- np.tan(phase_shift1) * I1
    # 复合信号重构
    S1=list()
    for idx in range(0,len(I1)):
        S1.append(complex(I1[idx]+QC1[idx]))
    S1 =np.array(S1)
    # 设定相关参数
    thread=20
    threadm=300
    Fs=1250
    L=len(S1)
    plt.rcParams['axes.unicode_minus'] = False

    sp=plt.specgram(S1,NFFT=80,Fs=1250,noverlap=40,detrend='linear')
    spec=np.array(sp[0])
    plt.colorbar()
    plt.xlabel('Time [sec]')
    plt.ylabel('Frequency [Hz]')
    




    rbvsdp=spec[20:38]+spec[42:60]
    rbvsdp=np.array(rbvsdp).transpose(1,0)
    pbc=np.zeros((rbvsdp.shape[0]))
    for idx in range(0,rbvsdp.shape[0]):
        pbc[idx]=np.sum(rbvsdp[idx])

    pbc=np.log(pbc+1)
    # 绘制柱状图
    fig, ax1 = plt.subplots()

    ax1.hist(pbc, bins=30, edgecolor='black', alpha=0.5)
    ax1.set_xlabel('pbc')
    ax1.set_ylabel('density')
    # 绘制曲线
    ax2 = ax1.twinx()

    x = np.linspace(min(pbc), max(pbc), 100)
    kde = stats.gaussian_kde(pbc)
    ax2.plot(x, kde(x), color='red')
    

    plt.show()
