import numpy as np
from scipy import signal
import os

list1=['lht0325','ljc0102','ljc1224']
list2=['curveleg','gettingup','left','right','wavehand']
for sub_dir1 in list1 :
    print(sub_dir1+'start')
    for sub_dir2 in list2:
        print(sub_dir2+'start')
        root_path = '../dataset/prv13'
        
        read_name1 = 'Radar1I.txt'
        read_name2 = 'Radar1Q.txt'
        read_name3 = 'Radar2I.txt'
        read_name4 = 'Radar2Q.txt'
        read_name5 = 'Tag.txt'

        w_name1='Radar1I_labal.txt'
        w_name2='Radar1Q_labal.txt'
        w_name3='Radar2I_labal.txt'
        w_name4='Radar2Q_labal.txt'

        read_path1 = os.path.join(root_path, sub_dir1,sub_dir2, read_name1)
        read_path2 = os.path.join(root_path, sub_dir1,sub_dir2, read_name2)
        read_path3 = os.path.join(root_path, sub_dir1,sub_dir2, read_name3)
        read_path4 = os.path.join(root_path, sub_dir1,sub_dir2, read_name4)
        read_path5 = os.path.join(root_path, sub_dir1,sub_dir2, read_name5)

        w_path1 = os.path.join(root_path, sub_dir1,sub_dir2, w_name1)
        w_path2 = os.path.join(root_path, sub_dir1,sub_dir2, w_name2)
        w_path3 = os.path.join(root_path, sub_dir1,sub_dir2, w_name3)
        w_path4 = os.path.join(root_path, sub_dir1,sub_dir2, w_name4)
        # 读取文本文件中的雷达数据
        s_radar_signal1I =  np.genfromtxt(read_path1, delimiter=',', filling_values=np.nan)
        s_radar_signal1Q =  np.genfromtxt(read_path2, delimiter=',', filling_values=np.nan)
        s_radar_signal2I =  np.genfromtxt(read_path3, delimiter=',', filling_values=np.nan)
        s_radar_signal2Q =  np.genfromtxt(read_path4, delimiter=',', filling_values=np.nan)
        radar_signaltag = np.genfromtxt(read_path5, delimiter=',', filling_values=0)

        fs=1250

        for start in radar_signaltag:

            if(start==0):break
            num_samples = int(fs * 3) # 采样率为 1250
            start_t = int(start)

            radar_signal1I= s_radar_signal1I[start_t:start_t+num_samples]
            radar_signal1Q= s_radar_signal1Q[start_t:start_t+num_samples]
            radar_signal2I= s_radar_signal2I[start_t:start_t+num_samples]
            radar_signal2Q= s_radar_signal2Q[start_t:start_t+num_samples]

            # 设定相关参数
            nperseg = 80
            noverlap = nperseg // 2

            # 计算功率谱密度并得到频谱图
            freqs, times, spectrogram1I = signal.spectrogram(radar_signal1I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='constant')
            freqs, times, spectrogram1Q = signal.spectrogram(radar_signal1Q, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='constant')
            freqs, times, spectrogram2I = signal.spectrogram(radar_signal2I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='constant')
            freqs, times, spectrogram2Q = signal.spectrogram(radar_signal2Q, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='constant')
        
            # 找到频谱图中高能部分的起始索引点和结束索引点
            threshold = 100000  # 阈值
            start_index1I = np.where(np.sum(spectrogram1I, axis=0) > threshold)[0][0] /91*3750+start_t
            end_index1I = np.where(np.sum(spectrogram1I, axis=0) > threshold)[0][-1]   /91*3750+start_t
            start_index1Q = np.where(np.sum(spectrogram1Q, axis=0) > threshold)[0][0]   /91*3750+start_t
            end_index1Q = np.where(np.sum(spectrogram1Q, axis=0) > threshold)[0][-1]  /91*3750+start_t
            start_index2I = np.where(np.sum(spectrogram2I, axis=0) > threshold)[0][0]   /91*3750+start_t
            end_index2I = np.where(np.sum(spectrogram2I, axis=0) > threshold)[0][-1]   /91*3750+start_t
            start_index2Q = np.where(np.sum(spectrogram2Q, axis=0) > threshold)[0][0]   /91*3750+start_t
            end_index2Q = np.where(np.sum(spectrogram2Q, axis=0) > threshold)[0][-1]  /91*3750+start_t
            
            # 将起始索引点和结束索引点写入文本文件
            with open(w_path1, 'a') as f:
                f.write(f"{int(start)}:{int(start_index1I)},{int(end_index1I)}\n")
            with open(w_path2, 'a') as f:
                f.write(f"{int(start)}:{int(start_index1Q)},{int(end_index1Q)}\n")
            with open(w_path3, 'a') as f:
                f.write(f"{int(start)}:{int(start_index2I)},{int(end_index2I)}\n")
            with open(w_path4, 'a') as f:
                f.write(f"{int(start)}:{int(start_index2Q)},{int(end_index2Q)}\n")
        print(sub_dir2+'over')
    print(sub_dir1+'over')