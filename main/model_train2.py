import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from skimage import exposure
import scipy.stats as stats
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import joblib
from sklearn.preprocessing import MinMaxScaler



fs=1250

list1=list()
root_path = '../dataset'
for root, dirs, files in os.walk(root_path):
    list1 = dirs
    break  
list2=['curveleg','gettingup','left','right','wavehand']
m_sum=0
r_sum=0
num=0
for sub_dir1 in list1 :
    num+=1
    print(num)
    print(sub_dir1+'-start')
    for sub_dir2 in list2:
        print(sub_dir1+'-'+sub_dir2+'-start')
        
        
        read_name1 = 'Radar1I.txt'
        read_name2 = 'Radar1Q.txt'
        read_name5 = 'Tag.txt'

        w_name1='FS1.txt'
        w_name3='FSlabel.txt'
        read_path1 = os.path.join(root_path, sub_dir1,sub_dir2, read_name1)
        read_path2 = os.path.join(root_path, sub_dir1,sub_dir2, read_name2)
        read_path5 = os.path.join(root_path, sub_dir1,sub_dir2, read_name5)
        num_w='0'
        root_path2='../datalabel'
        w_path1 = os.path.join(root_path2, num_w, w_name1)
        w_path3 = os.path.join(root_path2, num_w, w_name3)


        # 读取文本文件中的信号数据
        I1_s = np.genfromtxt(read_path1, delimiter=',', filling_values=0)
        Q1_s =  np.genfromtxt(read_path2, delimiter=',', filling_values=0)
        tag =np.genfromtxt(read_path5, delimiter=',', filling_values=0)


        def featureget(start, end):
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

            sp=plt.specgram(S1,NFFT=80,Fs=1250,noverlap=40)
            spec=np.array(sp[0])

            rbvsdp=spec[20:38]+spec[42:60]
            rbvsdp=np.array(rbvsdp).transpose(1,0)
            pbc=np.zeros((rbvsdp.shape[0]))
            for idx in range(0,rbvsdp.shape[0]):
                pbc[idx]=np.sum(rbvsdp[idx])

            pbc=np.log(pbc+1)
            u = pbc.mean()  # 计算均值
            std = pbc.std()  # 计算标准差
            # 绘制时频图
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Spectrogram')

            # 绘制pbc的分布图和拟合曲线
            n, bins, patches = ax2.hist(pbc, bins=100, density=True, alpha=0.5, edgecolor='black')
            mu, sigma = stats.norm.fit(pbc)
            best_fit_line = stats.norm.pdf(bins, mu, sigma)

            ax2.plot(bins, best_fit_line, 'r-', linewidth=2)
            ax2.set_xlabel('pbc values')
            ax2.set_ylabel('Probability density')
            ax2.set_title('Distribution of pbc')

            # 将拟合曲线绘制在柱状图上
            ax2_twinx = ax2.twinx()
            ax2_twinx.plot(bins, best_fit_line, color='red', linewidth=2)
            ax2_twinx.set_ylabel('Fitted Probability density', color='red')
            ax2_twinx.tick_params(axis='y', labelcolor='red')

            plt.tight_layout()
            plt.show()
            plt.close('all')

            res1,res2=stats.kstest(pbc, 'norm', (u, std))
            return res1,res2
        for i in tag:
            i=int(i)
            if(i==0):break
            w_res1,w_res2=featureget(i,i+fs*3)
            with open(w_path1, 'a') as f:
                f.write(f"{w_res1} {w_res2}\n")
            with open(w_path3, 'a') as f:
                f.write(f"{1}\n")
            w_res1,w_res2=featureget(i+fs*3,i+fs*4)
            with open(w_path1, 'a') as f:
                f.write(f"{w_res1} {w_res2}\n")
            with open(w_path3, 'a') as f:
                f.write(f"{0}\n")
        
    
    if(num%4==0):
        def read_feature(s_train_size=0.8, random_s=42):
            # 读取特征值和标签
            featureabove = np.loadtxt(w_path1)
            label = np.loadtxt(w_path3)
            # 将特征拼接为一个大的NumPy数组
            X = featureabove
            y = label
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - s_train_size, random_state=random_s)

            return X_train, X_test, y_train, y_test


        # 读取特征并划分数据集

        X_train, X_test, y_train, y_test = read_feature()

        # 定义LightGBM模型参数
        params = {
            'objective': 'multiclass',
            'num_class': 3,
            'metric': 'multi_logloss',
            
            "num_leaves": 31,
            'learning_rate': 0.05,
            'max_bin': 255,
            'force_col_wise': True,#使用并列计算
        }
        num_rounds = 100

        # 转换数据为LightGBM格式
        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test)

        # 训练LightGBM模型
        model = lgb.train(params, train_data, num_rounds, valid_sets=[test_data])

        # 在测试集上进行预测
        y_pred = model.predict(X_test)
        y_pred = np.argmax(y_pred, axis=1)


        # 计算准确率
        accuracy = np.sum(y_pred == y_test) / len(y_test)
        print(f"Accuracy: {accuracy}")

        joblib.dump(model, os.path.join(root_path2,num_w,str(num))+'Model.pkl')


