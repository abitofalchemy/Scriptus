#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys, string
import scipy, math
#from scipy.io.wavfile import read8
from scipy.signal import hann
from scipy.fftpack import fft
from scipy.fftpack import rfft
import matplotlib.pyplot as plt
import MySQLdb
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.lines import Line2D
import matplotlib.font_manager
# global sets
leg_prop = matplotlib.font_manager.FontProperties(size=14)
###################################

### This is the Gaussian data smoothing function I wrote ###
##  http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
##  code from SWHarden
def smoothListGaussian(list,degree=5):
    
    window=degree*2-1
    
    weight=np.array([1.0]*window)
    
    weightGauss=[]
    
    for i in range(window):
        
        i=i-degree+1
        
        frac=i/float(window)
        
        gauss=1/(np.exp((4*(frac))**2))
        
        weightGauss.append(gauss)
    
    weight=np.array(weightGauss)*weight
    
    smoothed=[0.0]*(len(list)-window)
    
    for i in range(len(smoothed)):  
        
        smoothed[i]=sum(np.array(list[i:i+window])*weight)/sum(weight)
    
    return smoothed

def showCharacteristics(matrixVar):
    print np.shape(matrixVar);
    shp = np.shape(matrixVar);
    print "[0]:",matrixVar[0,0]," [",shp[0]-1,"]:",matrixVar[shp[0]-1,0]," ms"
    fs = shp[0]/(matrixVar[shp[0]-1,0] -1)
    print "sampling frequency: ",fs
    return

def get_fft_mysql(email, cur):
    statement = """SELECT fft_result from TremCamTbl WHERE email =%s"""   
    try:
        cur.execute(statement,(email))
        results = cur.fetchall()
    except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
    return results

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height,
                 '%d'%int(height), ha='center', va='bottom')


def main():
    # input data
#    if (len(sys.argv) < 3):
#        print "Usage:   ./tremcam_timedomain.py hostname email[,email2]"
#        exit(0)
#    else:
#        host = sys.argv[1]
#        user = sys.argv[2]
    
    fig = plt.figure(1, figsize=(1.6*6,1*6))
    
    print len(sys.argv)
    eff_cores = np.zeros([10,6])
    eff_cores[:,0] = [12,24,80,144,200,288,360,500,700,1000]
    eff_cores[:,1] = [2, 4, 6, 8, 12, 24, 48, 256, 400, 0]
    eff_cores[:,2] = [2, 3, 9, 10,12, 14, 13, 16, 15,0 ]
    eff_cores[:,3] = [2, 3.5,10,11,13,14.5,13.5,15.5,17,0]
    eff_cores[:,4] = [5.2, 6.5,13.10,14.3,15,16.5,17.5,17.5,16,16.5]
    eff_cores[:,5] = [5, 6,13,14,15,14.5,16  ,17  ,16,15]
    
    N = 4
    
    menMeans = (20, 35, 30, 35)
    menStd =   (2, 3, 4, 1)
    womenMeans = (25, 32, 34, 20)
    womenStd =   (3, 5
                  , 2, 3)
    proMeans = (10, 25, 40, 45)
    proStd =   (2, 3, 4, 1)
    plaMeans = (15, 22, 44, 40)
    plaStd =   (3, 5, 2, 3)
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2       # the width of the bars
    print ind

    plt.subplot(111)
    rects1 = plt.bar(ind, menMeans, width,
                     color='r',
                     align='center',
                     yerr=menStd,
                     error_kw=dict(elinewidth=2, ecolor='gray'))

    
    rects2 = plt.bar(ind+width, womenMeans, width,
                     color='white',
                     align='center',
                     yerr=womenStd,
                     error_kw=dict(elinewidth=2, ecolor='gray'))

    rects3 = plt.bar(ind+width+width, proMeans, width,
                     color='black',
                     align='center',
                     yerr=proStd,
                     error_kw=dict(elinewidth=2, ecolor='gray'))
    rects4 = plt.bar(ind+3*width, plaMeans, width,
                     color='lightblue',
                     align='center',
                     yerr=plaStd,
                     error_kw=dict(elinewidth=2, ecolor='gray'))
    # add some
    plt.ylabel('Performance (ns/day) per 100 cores', fontsize=16)
    plt.title('MD Performance by Benchmark (Protein)')
    plt.xticks(ind+width, ('Alanine\nDipeptide', 'Hairpin', 'Proinsulin',
                           'Plasmepsin 4') )

    leg = plt.legend( (rects1[0], rects2[0], rects3[0],rects4[0]),
               ('AMBER-CPU', 'AMBER-GPU', 'AMOEBA-CPU','AMOEBA-GPU') ,fancybox=True, prop=leg_prop)
    
#    leg = plt.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)
    
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)

    x1,x2,y1,y2 = plt.axis()
    plt.axis([-.1*x2,x2,y1,y2*1.3])
    plt.draw()
    ## generate an image file
    fig = plt.gcf()
    DPI = fig.get_dpi()
    fig.savefig('images/figplot.png',dpi = (300))
    
    # Figure 2
# setup plot
    fig2 = plt.figure(2, figsize=(1.6*6,1*6))
#    fig = plt.figure()
    fig2 = plt.gcf()
    ax1 = fig2.add_subplot(111)
    #ax1.minorticks_on()
#    ax2 = fig.add_subplot(212)
#    ax2.minorticks_on()
    ax1.set_xlabel("Cores",fontsize=16)
    ax1.set_ylabel("Performance Efficiency (ns/day)", fontsize=16)
#    ax2.set_xlabel("CPU Cores")
#    ax2.set_ylabel("Performance Efficiency (ns/day)")
#    ax1.axis('off')
#    ax1.set_frame_on(False)
    ax1.get_xaxis().tick_bottom()
#    ax1.axes.get_yaxis().set_visible(False)
    xmin, xmax = ax1.get_xaxis().get_view_interval()
    ymin, ymax = ax1.get_yaxis().get_view_interval()
    ax1.plot(eff_cores[0:9,1],eff_cores[0:9,2],'-ro', linewidth=2.0,label='$CPU$-AMOEBA')
    ax1.plot(eff_cores[0:9,1],eff_cores[0:9,3],'-ks', linewidth=2.0,label='$CPU$-AMBER')
    ax1.plot(eff_cores[:,0],eff_cores[:,4],'-bD', linewidth=2.0,label='$GPU$-AMOEBA')
    ax1.plot(eff_cores[:,0],eff_cores[:,5],'-g^', linewidth=2.0,label='$GPU$-AMBER')
    leg = ax1.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
    leg.get_frame().set_alpha(0.5)
#    leg2 = ax2.legend(loc='best', shadow=True, fancybox=True, prop=leg_prop)
#    leg2.get_frame().set_alpha(0.5)
#    mu, sigma=100, 15
#    x=mu + sigma*np.random.randn(10000)
#    hist,bins=np.histogram(x,bins=4)
#    width=0.7*(bins[1]-bins[0])
#    center=(bins[:-1]+bins[1:])/2
    #ax1.bar(center,hist,align='center',width=width)
    
    ## generate an image file
    fig2 = plt.gcf()
    DPI = fig2.get_dpi()
    fig2.savefig('images/figplot.png',dpi = (300))


    

## main
if __name__ == '__main__':
    main()


#query = "SELECT accelX FROM TremCamTbl WHERE email='saguinag@nd.edu'"
#cursor.execute(query)
#result = cursor.fetchall()
#input_data = []
#for record in result:
#    print "len(record)" , len(record)
#    if len(record)>0:
#        input_data.append(record[0])
#    
#input_data = read("cello.wav")
#print len(input_data)
#audio = input_data[0]
#for i in (range(10)):
#	print i,":",audio[100+i]
#
#N=len(audio)
#print "N=len(audio):",N
### plot time domain data
#plt.plot(audio)
#plt.ylabel("Amplitude")
#plt.xlabel("Time (samples)")
## set the title
#plt.title("Accelerometer X-axis")
#plt.show()
