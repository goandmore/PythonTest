import matplotlib.pyplot as plt
import math
import time
import win32api,win32con

x_screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) #获得屏幕分辨率X轴

y_screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) #获得屏幕分辨率Y轴

#1366/768 = 1.78   Display size scale
display_size_scale = round(x_screen_width/y_screen_height,2)

def splitPrimeAndCombined(num):
    prime=[]
    combined=[]
    for i in range(500,num):
        square_num = math.floor(i**0.5)
        for j in range(2,(square_num+1)):
            if(i % j) == 0:
                combined.append(i)
                break
        else:
            prime.append(i)

    return prime,combined

def onlycombined(s):
    tx=[]
    ty=[]
    for i in s:
        tx.append(i*math.sin(i))
        ty.append(i*math.cos(i))
    return tx,ty

def displayPrimes():

    inputnumStr = input("please input a num(which is greater than 500):")
    if not inputnumStr.isdigit():
        exit()

    inputnum = int(inputnumStr)

    #prime num and combined num
    prime,combined=splitPrimeAndCombined(inputnum)

    #prime num coordinate
    sinx=[]
    cosx=[]
    #combined num coordinate
    siny=[]
    cosy=[]

    for i in prime:
        sinx.append(i*math.sin(i))
        cosx.append(i*math.cos(i))

    for i in combined:
        siny.append(i*math.sin(i))
        cosy.append(i*math.cos(i))

    #only combined num spiral arms
    s1= [514]
    s2= [517]
    s3= [520]
    s4= [536]
    s5= [539]
    s6= [542]

    while s6[-1] <= inputnum:
        s1.append(s1[-1]+44)
        s2.append(s2[-1]+44)
        s3.append(s3[-1]+44)
        s4.append(s4[-1]+44)
        s5.append(s5[-1]+44)
        s6.append(s6[-1]+44)

    plt.scatter(cosx,sinx,c="red",s=2)   #prime
    plt.scatter(cosy,siny,c="blue",s=2)  #combined
    tx,ty=onlycombined(s1)
    plt.plot(ty,tx,c="y")
    tx,ty=onlycombined(s2)
    plt.plot(ty,tx,c="y")
    tx,ty=onlycombined(s3)
    plt.plot(ty,tx,c="y")
    tx,ty=onlycombined(s4)
    plt.plot(ty,tx,c="y")
    tx,ty=onlycombined(s5)
    plt.plot(ty,tx,c="y")
    tx,ty=onlycombined(s6)
    plt.plot(ty,tx,c="y")

    plt.xlim(-display_size_scale*inputnum,display_size_scale*inputnum)
    plt.ylim(-inputnum,inputnum)
    plt.axis()

    #plt.savefig("images/primedistrib%s.png"%time.time())
    # plt.get_current_fig_manager().full_screen_toggle()
    plt.get_current_fig_manager().window.state('zoomed')    #maximum display
    plt.show()



#main thread
while True:
    displayPrimes()