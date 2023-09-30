import math
from scipy import signal
import numpy as np


def filtrate(signals):
    order = 4
    # b, a = signal.butter(order, [2 / 1250 * 2], 'highpass')  # 2Hz 高通
    # filtered_signals = signal.filtfilt(b, a, signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 49, 2 / 1250 * 51], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 99, 2 / 1250 * 101], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 149, 2 / 1250 * 151], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 199, 2 / 1250 * 201], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 249, 2 / 1250 * 251], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 299, 2 / 1250 * 301], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 349, 2 / 1250 * 351], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 399, 2 / 1250 * 401], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 449, 2 / 1250 * 451], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 499, 2 / 1250 * 501], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 549, 2 / 1250 * 551], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    # b, a = signal.butter(order, [2 / 1250 * 599, 2 / 1250 * 601], 'bandstop')
    # filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    b, a = signal.butter(order, [2 / 1250 * 2], 'highpass')  # 2Hz 高通
    filtered_signals = signal.filtfilt(b, a, signals)  # data为要过滤的信号
    for idx in range(1, 13):
        b, a = signal.butter(order, [2 / 1250 * (50*idx - 1), 2 / 1250 * (50*idx + 1)], 'bandstop')  # 配置滤波器 8 表示滤波器的阶数
        filtered_signals = signal.filtfilt(b, a, filtered_signals)  # data为要过滤的信号
    return filtered_signals


def calibrate(channel_i, channel_q, gain_ratio, angle):
    calibrated_q = [0]*len(channel_i)
    for i in range(0, len(channel_i)):
        # calibrated_q[i] = gain_ratio/math.cos(angle)*channel_q[i]-math.tan(angle)*channel_i[i]
        calibrated_q[i] = gain_ratio / math.cos(angle) * channel_q[i] - math.tan(angle) * channel_i[i]
    return calibrated_q


def combine(channel_i, channel_q):
    rtn = np.zeros(len(channel_i), dtype=complex)
    for i in range(0, len(channel_i)):
        rtn[i] = complex(channel_i[i], channel_q[i])
    return rtn


def estimate_parameters(channel_i, channel_q):
    scale = max(channel_i) - min(channel_i)
    n = len(channel_i)
    M = np.zeros((n, 5), dtype=np.float64)
    N = np.zeros((n, 1), dtype=np.float64)
    print(scale)
    for i in range(0, n):
        M[i][0] = channel_q[i]*channel_q[i]/scale/scale
        M[i][1] = channel_i[i] * channel_q[i]/scale/scale
        M[i][2] = channel_i[i]/scale
        M[i][3] = channel_q[i]/scale
        M[i][4] = 1
        N[i][0] = -channel_i[i]*channel_i[i]/scale/scale
    a = np.matmul(np.matmul(np.linalg.inv(np.matmul(M.transpose(), M)), M.transpose()), N)
    print(a)
    DCQ = (a[1][0]*a[2][0]-2*a[3][0])/(4*a[0][0]-a[1][0]*a[1][0])
    print('DCQ', DCQ)
    DCI = (2*a[0][0]*a[2][0]-a[1][0]*a[3][0])/(a[1][0]*a[1][0]-4*a[0][0])
    print('DCI', DCI)
    angle = math.asin(-a[1][0]/math.sqrt(a[0][0])/2)
    print('angle', angle)
    AI = math.sqrt((DCI*DCI + a[0][0]*DCQ*DCQ - a[1][0]*DCI*DCQ - a[4][0])/(1-a[1][0]*a[1][0]/4/a[0][0]))
    print('AI', AI)
    AQ = math.sqrt(AI*AI/a[0][0])
    print('AQ', AQ)
    # return DCI, DCQ, AI, AQ, angle#角度为弧度
    return 0


def perform_stft(sig, fs, win, overlap):
    _f, _t, _zxx = signal.stft(sig, fs=fs, window='hann', nperseg=win, noverlap=overlap, nfft=win, detrend=False, return_onesided=False, padded=False, boundary=None)
    t_size = len(_t)
    _mid = len(_f) // 2
    for i in range(_mid):
        _temp = _f[i]
        _f[i] = _f[i+_mid]
        _f[i+_mid] = _temp
    image = np.zeros(_zxx.shape, dtype=complex)
    for vvidx in range(0, _mid):
        for vvidy in range(0, t_size):
            image[vvidx][vvidy] = _zxx[vvidx + _mid][vvidy]
            image[vvidx + _mid][vvidy] = _zxx[vvidx][vvidy]
    return _f, _t, image


if __name__ == '__main__':
    # x = 2 * np.pi * np.arange(10000) / 10000
    # signal_i = np.zeros(10000)
    # signal_q = np.zeros(10000)
    # for i in range(0, len(x)):
    #     signal_i[i] = math.cos(x[i]) + 0.15
    #     signal_q[i] = 1.5 * math.sin(x[i] + 0.2) - 0.15
    # DCI, DCQ, AI, AQ, angle = estimate_parameters(signal_i, signal_q)
    # print(DCI)
    # print(DCQ)
    # print(AI)
    # print(AQ)
    # print(angle)
    f = open('./calibration/above/Radar1I.txt', "r")  #
    aboveI = list(map(int, f.read().strip(',').split(',')))
    f.close()
    f = open('./calibration/above/Radar1Q.txt', "r")  #
    aboveQ = list(map(int, f.read().strip(',').split(',')))
    f.close()
    f = open('./calibration/side_1/Radar2I.txt', "r")  #
    side1I = list(map(int, f.read().strip(',').split(',')))
    f.close()
    f = open('./calibration/side_1/Radar2Q.txt', "r")  #
    side1Q = list(map(int, f.read().strip(',').split(',')))
    f.close()
    f = open('./calibration/side_2/Radar2I.txt', "r")  #
    side2I = list(map(int, f.read().strip(',').split(',')))
    f.close()
    f = open('./calibration/side_2/Radar2Q.txt', "r")  #
    side2Q = list(map(int, f.read().strip(',').split(',')))
    f.close()
    print("Parameters for above radar: DCI, DCQ, AI, AQ, angle")
    print(estimate_parameters(aboveI, aboveQ))
    # print("Parameters for side1 radar: DCI, DCQ, AI, AQ, angle")
    # print(estimate_parameters(side2I, side1Q))
    # print("Parameters for side2 radar: DCI, DCQ, AI, AQ, angle")
    # estimate_parameters(side2I, side2Q)
