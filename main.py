"""水文与软件工程测试项目"""
'''读取关于项目的数据'''
'''2024年05月27日 厉福超组'''
'''1.0.0.0'''
"""输入 逐日蒸发量（potential evapotranspiration），
    逐日降雨量（rainfall depth，areal catchment rainfall）
    模型输出：流域出口断面逐日径流量    Q
    *****************************
    模型参数：：
            x1：产流水库容量（mm）
            x2：地下水交换系数（mm）
            x3：汇流水库容量（mm）
            x4：单位线汇流时间（天）
    模型状态：En，Pn，Es，Ps，Perc,Pr,R,Qr,Qd
    GR4J是日模型，根据每天降雨量蒸发量更新汇流状态
    GR4J建模三步骤：
                1.Interception（拦截）
                2.Production store（产流）
                3.Routing store（汇流）
    第一阶段 E:日蒸发 P：日降雨-------->拦截量(En ,(Pn))--->Pn产生Ps和Pn-Ps
                      Pn-Ps----->Pr
                      Pr与收集的水算出Perc
"""
import numpy as np
def SH1_CURVE(t,x4):                #S曲线
    if t<0.0:
        sh=0.0
    elif t<x4:
        sh=(t/x4)**2.5
    elif t>x4:
        sh=1.0
    return sh
def SH2_CURVE(t,x4):                #S曲线
    if t<0.0:
        sh=0.0
    elif t<x4:
        sh=0.5*(2-t/x4)**2.5
    elif t>x4:
        sh=1.0
    return sh

para = np.loadtxt("data/Riverdata.txt")
data = np.loadtxt("data/Riverdata.txt")
x1=float(para[0])
x2=float(para[1])
x3=float(para[2])
x4=float(para[3])
'''定义P E数组
    降雨量>蒸发量 pn-p-e（邮箱有效降雨），净蒸发en=0
    降雨量<蒸发量 Pn=0 （有效降雨）    ，净蒸发en=e-p，    
'''
nStep=data.shape[0]
Pn=np.zeros(nStep)          #定义数组，降雨量
En=np.zeros(nStep)          #蒸发能力



maxDayDelay =10               #计算根据x4计算s曲线和单位线，假设单位长度UHI%10,UH2%20天
# 计算sh1以及sh2
SH1=np.zeros(maxDayDelay)     #定义第一条单位线的累计曲线
UH1=np.zeros(maxDayDelay)     #定义第一条单位线
SH2=np.zeros(maxDayDelay*2)   #定义第二条单位线的累计曲线
UH2=np.zeros(maxDayDelay*2)   #定义第二条单位线
# 计算SH1 AND SH2
for i in range(maxDayDelay):
    SH1[i]=SH1_CURVE(i,x4)
    print(SH1)
for i in range(maxDayDelay*2):
    SH2[i] = SH2_CURVE(i,x4)

#计算UH1 以及 UH2
for i in range(maxDayDelay):
    if i==0:
        UH1[i]=SH1[i]
    else:
        UH1[i] = UH1[i]-SH1[i]
for i in range(maxDayDelay*2):
    if i==0:
        UH2[i]=SH2[i]
    else:
        UH2[i] = UH2[i]-SH2[i]

P=np.zeros(10)
E=np.zeros(10)
for i in range(nStep):
    if P[i]>=E[i]:
        Pn[i]=P[i]-E[i]
        E[i]=0;
    else:
        Pn[i]=0
        En[i]=E[i]-P[i]             #判断蒸发 降雨之间的关系
#Q    =simulate_gr4j(nstep)

"""如上是单位线"""
simulate_gr4j(nStep,x1,x2,x3,x4,upperTankRation,lowerTankRation,maxDayDelay,HU1,HU2,Pn,En)