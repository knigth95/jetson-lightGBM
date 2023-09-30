import numpy as np
from scipy import signal
import os


def save_all_folder_names(root_path):
    folder_names = []
    for foldername, subfolders, files in os.walk(root_path):
        if foldername != root_path:
            break
        for subfolder in subfolders:
            if not subfolder.startswith('mm'):   #过滤掉以"mm"开头的文件夹
                folder_names.append(subfolder)

    '''with open('folder_names.txt', 'w') as f:
        for folder_name in folder_names:
            f.write(folder_name + '\n')
    '''
    return folder_names
print(save_all_folder_names('./dataset/'))

list1=save_all_folder_names('./dataset/')
#list1=['lht0325']
list2=['curveleg','gettingup','left','right','wavehand']
for sub_dir1 in list1 :
    print(sub_dir1+'start')
    for sub_dir2 in list2:
        print(sub_dir2+'start')
        root_path = './dataset/'
        
        read_name1 = 'Radar1I.txt'
        read_name5 = 'Tag.txt'

        w_name1='Labal_Change'
       

        read_path1 = os.path.join(root_path, sub_dir1,sub_dir2, read_name1)
        read_path5 = os.path.join(root_path, sub_dir1,sub_dir2, read_name5)

        w_path1 = os.path.join(root_path, sub_dir1,sub_dir2, w_name1)
        # 读取文本文件中的雷达数据
        s_radar_signal1I =  np.genfromtxt(read_path1, delimiter=',', filling_values=np.nan)
        radar_signaltag = np.genfromtxt(read_path5, delimiter=',', filling_values=0)

        fs=1250


        for start in radar_signaltag:

            if(start==0):break
            num_samples = int(fs * 3) # 采样率为 1250
            start_t = int(start)

            radar_signal1I= s_radar_signal1I[start_t:start_t+num_samples]

            # 设定相关参数
            nperseg = 80
            noverlap = nperseg // 2

            # 计算功率谱密度并得到频谱图
            freqs, times, spectrogram1I = signal.spectrogram(radar_signal1I, fs=fs, window='hamming', nperseg=nperseg, noverlap=noverlap, detrend='constant')
        

            sum=np.sum(spectrogram1I,axis=0) #每列求和
            threshold = np.mean(sum)  # 平均值
            print(threshold)
            # 找到频谱图中高能部分的起始索引点和结束索引点
            '''
            sum=0
            for i in range(start_t,start_t+num_samples+1):
                sum=sum+int(s_radar_signal1I[i])
            threshold = int(sum/3751)  # 平均值
            '''
            indices = np.where(np.sum(spectrogram1I, axis=0) > threshold)[0]
            if len(indices) == 0:
                print("未找到满足条件的索引，请检查阈值设置或输入数据。")
                with open(w_path1+'(wrong).txt', 'a') as f:
                    f.write(f"[‘未找到满足条件的索引’]:{int(start)}\n")
                continue
            else:
                start_index1I = np.where(np.sum(spectrogram1I, axis=0) > threshold)[0][0] /91*3750+start_t
                end_index1I = np.where(np.sum(spectrogram1I, axis=0) > threshold)[0][-1]   /91*3750+start_t
                # 将起始索引点和结束索引点写入文本文件
                with open(w_path1+'.txt', 'a') as f:
                    f.write(f"{int(start_index1I)},{int(end_index1I)}\n")
            '''
            test_z=(start_index1I-start)/1250
            test_m=(end_index1I-start)/1250
            print("起始："+str(test_z))
            print("结束："+str(test_m))
            print(f"{int(start)}:{int(start_index1I)},{int(end_index1I)}\n")    
            with open('./duibi.txt','a') as f:
                f.write(f"{'起始'}:{str(test_z)},{'结束'}:{str(test_m)}\n")
                f.write(f"{int(start)}:{int(start_index1I)},{int(end_index1I)}\n")
            '''
        print(sub_dir2+'over')
    print(sub_dir1+'over')
