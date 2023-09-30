from __future__ import print_function
import sys
import time
import Jetson.GPIO as GPIO
import spidev
import numpy as np
import threading
import queue
import joblib
import pickle
from scipy import stats

from numpy.distutils import show_config

import matplotlib.pyplot as plt
from lightgbm import LGBMClassifier

class ads131m04:
    def __init__(self,spidevnum0,spidevnum1,DataSaveNum=1250*5):        
        self.I1=list()
        self.Q1=list()
        self.I2=list()
        self.Q2=list()
        self.MaxRadarDataNum=DataSaveNum
        self.radarData=0
        self.dRDY_pin = 18
        self.led_pin = 26
        self.reset_pin = 16
        self.spihandle=spidev.SpiDev()
        self.spihandle.open(spidevnum0,spidevnum1)
        self.spihandle.max_speed_hz=10500000
        self.spihandle.mode=0b01
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.dRDY_pin, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.reset_pin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.output(self.reset_pin,GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.reset_pin,GPIO.HIGH)
        time.sleep(0.1)
        self.setRegData(0x03,0xF02)
        readdata=self.getRegData(18)     

    def LED_Off():
        GPIO.cleanup(self.led_pin)
        GPIO.output(self.led_pin,GPIO.HIGH)
    def LED_On():
        GPIO.cleanup(self.led_pin)
        GPIO.output(self.led_pin,GPIO.LOW)


    def setRegData(self,Reg,Data):   
        self.spihandle.writebytes([Reg,Data])
        return True
    def getRegData(self,num):        
        return self.spihandle.readbytes(num)

    def bitOp(self,num,tms):
        x=bin(num)
        for i in range(0,tms):
            x=x+'0'
        return int(x,2)
           
    def dRDYOK(self):
        if GPIO.input(self.dRDY_pin)==GPIO.LOW:
            return True
        return False
    def transRadarData(self):
        if self.dRDYOK()==False:
            return False
        readdata=self.getRegData(18)
        self.I1.append(self.bitOp(readdata[3],16) +self.bitOp(readdata[4],8) +readdata[5])
        self.Q1.append(self.bitOp(readdata[6],16) +self.bitOp(readdata[7],8) +readdata[8])
        self.I2.append(self.bitOp(readdata[9],16) +self.bitOp(readdata[10],8) +readdata[11])
        self.Q2.append(self.bitOp(readdata[12],16) +self.bitOp(readdata[13],8) +readdata[14])
        if (len(self.I1)>self.MaxRadarDataNum):
            self.I1.pop(0)
            self.Q1.pop(0)
            self.I2.pop(0)
            self.Q2.pop(0)
        return True
    def getRadarData(self,DataNum=1250):
        if DataNum<=self.MaxRadarDataNum:
            return self.I1[len(self.I1)-DataNum:],self.Q1[len(self.Q1)-DataNum:],self.I2[len(self.I2)-DataNum:],self.Q2[len(self.Q2)-DataNum:]
        else:
            return -1,-1,-1,-1
    def close(self):        
        self.spihandle.close()        
        GPIO.cleanup()

def get_ADS131_Data(Fs=1250):
    global ads
    while True:
        lock_ADs.acquire()
        ads.transRadarData()
        lock_ADs.release()
        time.sleep(1/Fs)

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


ads=ads131m04(0,0)
GPIO.setwarnings(False)
if __name__ == '__main__':
    sampling_Fs=1250          #adc sampling frequency
    detect_Fs=3              #detect target frequency    
    print('1')
    th_ADS=threading.Thread(target=get_ADS131_Data,args=(sampling_Fs,))
    lock_ADs =threading.Lock()
    th_ADS.start()   
    time.sleep(detect_Fs/sampling_Fs)   #wait ads131 get enough adc num
    print('2')    
    # twoclf=joblib.load('./train_model/twoRadarModel.pkl')
    
    with open('./train_model/aboveRadarModel.pkl', 'rb') as fin:
        aboveclf=pickle.load(fin)
        
    # aboveclf=joblib.load('./train_model/aboveRadarModel.pkl')
    # sideclf=joblib.load('./train_model/sideRadarModel.pkl')
    print('3')     
    while True:
        time.sleep(1/detect_Fs)
        lock_ADs.acquire()
        radar_I1,radar_Q1,radar_I2,radar_Q2=ads.getRadarData(DataNum=sampling_Fs)
        lock_ADs.release()
        if -1 in radar_I1:            
            continue        
        # print(radar_I1)
        sig1=list()
        sig2=list()
        for idx in range(0,len(radar_I1)):
            sig1.append(complex(radar_I1[idx]+radar_Q1[idx]))
            sig2.append(complex(radar_I2[idx]+radar_Q2[idx]))
        # sig1=complex(radar_I1,radar_Q1)
        # sig2=complex(radar_I2,radar_Q2)
        sig1=np.array(sig1)
        sig2=np.array(sig2)
        
        sig1=torch.from_numpy(sig1)
        sig1=torch.from_numpy(sig1).unsqueeze(1)
        sig2=torch.from_numpy(sig2)
        sig2=torch.from_numpy(sig2).unsqueeze(1)
        
        
        sig1_feature_1,sig1_feature_2=getDensity(sig1)
        sig2_feature_1,sig2_feature_2=getDensity(sig2)
        print('detect')
        # print(sig1_feature_1)
        # print(sig1_feature_2)
        # print(sig2_feature_1)
        # print(sig2_feature_2)
        # if twoclf.predit([sig1_feature_1,sig1_feature_2,sig2_feature_1,sig2_feature_2]):
        #     ads.LED_On()
        #     print('target Move Two')
        # else:
        #     ads.LED_Off()
        #     print('target stay Two')
                
        if aboveclf.predit([sig1_feature_1,sig1_feature_2]):
            ads.LED_On()
            print('target Move Above')
        else:
            ads.LED_Off()
            print('target stay Above')
                
        # if sideclf.predit([sig2_feature_1,sig2_feature_2]):
        #     # ads.LED_On()
        #     print('target Move Side')
        # else:
        #     # ads.LED_Off()
        #     print('target stay Side')
        
        
    for idx in range(0,Fs*time_second):
        if ads.transRadarData():
            I1.append(ads.I1)
            Q1.append(ads.Q1)
            I2.append(ads.I2)
            Q2.append(ads.Q2)    
        # else:
        #     print('not ready.')
        time.sleep(1/Fs)
    ads.close()

    def saveRadarData(name,radarData): 
        fileName='radarData/'+name+'.txt'
        f=open(fileName,'w')
        for x in radarData:
            f.write(str(x))
            f.write(',')
        f.close()
    I1=np.array(I1)
    Q1=np.array(Q1)
    I2=np.array(I2)
    Q2=np.array(Q2)
    saveRadarData('I1',I1)
    saveRadarData('Q1',Q1)
    saveRadarData('I2',I2)
    saveRadarData('Q2',Q2)
    
