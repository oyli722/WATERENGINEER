import numpy as np


def simulate_gr4j(nStep,x1,x2,x3,x4,upperTankRatio,lowerTankRation,maxDayDelay,HU1,HU2,Pn,En):
    """#定义产汇流相关参数"""
    S0=upperTankRatio*x1                #产流水库初始含水量
    R0=lowerTankRation * x1             #汇流水库初始土壤含量=初始土壤含水量笔记*汇流水库容量
    R_temp=R0
    S_temp=S0                           #用s_temp记录存储产流水库当前含水量
    S=np.zeros(nStep)                   #产流水库数组，每个元素记录当前含水量
    R = np.zeros(nStep)                 #汇流水库数组，数组中每个元素记录当天的途昂含水量
    R_fast=np.zeros(nStep)
    R_slow=np.zeros(nStep)
    UH_Fast=np.zeros(nStep,maxDayDelay)
    UH_Slow = np.zeros(nStep, 2*maxDayDelay)
    Ps = np.zeros(nStep)                # 产流中间变量，指每天有多少水补充土壤含水量
    Es = np.zeros(nStep)                   # 产流中间变量，指每天有多少水蒸发土壤含水量
    Perc =np.zeros(nStep)               #每天土壤下渗产生的径流
    Pr=np.zeros(nStep)                  #hr4j模型总产流量
    F=np.zeros(nStep)                   #汇流中间变量。记录每天地表水和地下水的量
    Qr=np.zeros(nStep)                  #汇流快速流产流量，每天
    Qd=np.zeros(nStep)                  #汇流慢速
    Q=np.zeros(nStep)                   #每天截面流量
    for i in range(nStep):
        S[i]=S_temp
        R[i]=R_temp
        #使用Pn[i]AND En[i]来进行判断
        if Pn!=0 :
            Ps[i]=x1*(1-((S[i]/x1)**2)*np.tanh(Pn[i]/x1)(1+S[i])/x1*np.tanh(Pn[i]/x1))
            Es[i]=0
        if En[i]!=0:
            Es[i]=(S[i]*(2-(S[i]/x1))*np.tanh(En[i]/x1))/(1+(1-S[i]/x1)*np.tanh(En[i]/x1))
        S_temp=S_temp-Es[i]+Ps[i]
        Perc[i]=S_temp*(1-(1+(4.0/9.0*(S_temp/x1))**4)**(-0.25))                             #计算每天的Perc
        #计算产流量
        Pr[i]=Perc[i]+(Pn[i]-Ps[i])
        #更新产流水库的土壤含水量
        S_temp=S_temp-Perc[i]
        R_fast=0.9*Pr[i]            #快速水流 HU1单位线
        R_slow=0.1*Pr[i]
        #进行汇流计算
        if i==0:
            UH_Fast[i,:]=R_fast*HU1         #第一时段的出流过程先，快速流动
            UH_Slow[i,:]=R_slow*HU2         #第一个时段的出流过程线，慢速流动
        else :
            UH_Fast[i,:]=R_fast*HU1
            for j in range(maxDayDelay-1):
                UH_Slow[i,j]=UH_Fast[i,j]+UH_Fast[i-1,j-1] #第二时段总汇流=+第一时段错峰产量
            UH_Slow[i,:]=R_slow*HU2
            for j in range(2*maxDayDelay-1):
                UH_Slow[i,j]=UH_Slow[i,j]+UH_Slow[i-1,j+1]
        F[i]=x2*(R[i]/x3)**3.5
        #更新汇流水库水量变化
        R_temp=max(0,R_temp+UH_Fast[i,1]+F[i])
        #计算汇流水库快速流出流量
        Qr[i]=R_temp*(1-(1+R_temp/x3)**4)**2.5


