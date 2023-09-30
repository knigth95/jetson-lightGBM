import time
import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import pandas as pd
import os


def main():
    f = None
    fo = None
    fl = None
    root = ''+os.path.dirname(__file__)+'/dataset/'
    nextMotion = ['curveleg/', 'gettingup/','left/', 'right/', 'wavehand/']
    
    nextFile=os.listdir(root)
    for i in range(0,len(nextFile)):
        nextFile[i]=nextFile[i]+'/'
        

    for i in range(0, len(nextFile)):
        for j in range(0, 5):
            if nextFile[i][0]!='m':         #为了排除m开头文件的影响
                motion1 = nextFile[i]
                motion2 = nextMotion[j]

                ls = open(root+motion1+motion2+"Tag.txt").readlines()
                newTxt = ""
                for line in ls:
                    newTxt = newTxt+" ".join(line.split(","))+"\n"
                fo = open(root+motion1+motion2+"Tagout.txt", "x")
                fo.write(newTxt)
                fo.close()

                data_txt = np.loadtxt(root+motion1+motion2+"Tagout.txt")
                data_txtDF = pd.DataFrame(data_txt)
                data_txtDF.to_csv(root+motion1+motion2+"Tag.csv", index=False)
                print("ok")
                with open(root+motion1+motion2+"0.5-2.2tag.txt", mode='w') as fo:
                    with open(root+motion1+motion2+"Tag.csv", mode='r') as fl:
                        for num1 in fl.read().splitlines():
                            number1 = int(float(num1))
                            if number1 != 0:
                                fo.write("%d" % (number1+0.5*1250))
                                fo.writelines(",")
                                fo.write("%d" % (number1+2.2*1250))
                                fo.write('\n')
                        time.sleep(0.5)
                        print("success-"+root+motion1+motion2+"(0.5-2.2tag).txt")
                    fl.close()
                fo.close()
                os.remove(root+motion1+motion2+"Tagout.txt")
                os.remove(root+motion1+motion2+"Tag.csv")
            
if __name__ == '__main__':
    main()
