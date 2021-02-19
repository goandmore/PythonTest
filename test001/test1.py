
import matplotlib.pyplot as plt
import math
import time

inputnum = int(input("plz input a num:"))

#prime num
X=[]
#combined num
Y=[]

for i in range(500,inputnum):

    square_num = math.floor(i**0.5)
    for j in range(2,(square_num+1)):
        if(i % j) == 0:
            Y.append(i)
            break
        
    else:
        X.append(i)



#prime num
#x=[]  #minus
sinx=[]
cosx=[]
#combined num
#y=[]  #minus
siny=[]
cosy=[]

for i in X:
    #x.append(-i)
    sinx.append(i*math.sin(i))
    cosx.append(i*math.cos(i))

for i in Y:
    #y.append(-i)
    siny.append(i*math.sin(i))
    cosy.append(i*math.cos(i))


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

def onlycombined(s):
    tx=[]
    ty=[]
    for i in s:
        tx.append(i*math.sin(i))
        ty.append(i*math.cos(i))
    return tx,ty

plt.scatter(cosx,sinx,c="red",s=2)   #prime
plt.scatter(cosy,siny,c="blue",s=2)  #combined
tx,ty=onlycombined(s1)
plt.plot(ty,tx,c="g")
tx,ty=onlycombined(s2)
plt.plot(ty,tx,c="g")
tx,ty=onlycombined(s3)
plt.plot(ty,tx,c="g")
tx,ty=onlycombined(s4)
plt.plot(ty,tx,c="g")
tx,ty=onlycombined(s5)
plt.plot(ty,tx,c="g")
tx,ty=onlycombined(s6)
plt.plot(ty,tx,c="g")

#1680/1050 = 1.6   Display size

plt.xlim(-1.6*inputnum,1.6*inputnum)
plt.ylim(-inputnum,inputnum)
plt.axis()


#plt.savefig("images/primedistrib%s.png"%time.time())
plt.show()
