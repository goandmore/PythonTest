import cProfile
import math

inputnum = int(input("please input a number:"))

def IfPrime1(num):
    if num >1:
        for i in range(2,num):
            if(num%i)==0:
                print(num,"is combined number")
                print(i,"multiply",num//i,"equal",num)
                break
            if i==num-1:
                print(num,"is prime number")
    else:
        print(num,"is combined number")

def IfPrime2(num):
    # 用户输入数字
    # 质数大于 1
    if num > 1:
        # 找到其平方根（ √ ），减少算法时间
        square_num = math.floor( num ** 0.5 )
        # 查找其因子
        for i in range(2, (square_num+1)): #将平凡根加1是为了能取到平方根那个值
            if (num % i) == 0:
                print(num, "is combined number")
                print(i, "multiply", num // i, "equal", num)
                break
        else:
            print(num, "is prime number")
            # 如果输入的数字小于或等于 1，不是质数
    else:
        print(num, "is not prime or combined number")

cProfile.run('IfPrime1(inputnum)')
cProfile.run('IfPrime2(inputnum)')

#swap test
a=58
b=189

print("a:%d"%a,"b:%d"%b)

a=a^b
b=a^b
a=b^a

print("a:%d"%a,"b:%d"%b)

