def evaluate_gr4j_model(nStep,Qobs_mm,Q)
    count=0 #计数器
    Q_accum=0.0#记录累计径流量
    Q_ave=0.0 #记录平均径流量
    NSE=0.0 #记录那身效率
    Q_diff1=0.0
    Q_diff2=0.0
    for i in range(365,nStep):

