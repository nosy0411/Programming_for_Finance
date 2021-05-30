import numpy as np
import math
import matplotlib.pyplot as plt
import os
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
path = r'C:\\Users\\inventor\\Desktop\\FR study\\FR-30th\\Derivatives_study\\FR_30_NIH\\ing'
os.chdir(path)
 
# 위험 중립 세계에서 u와 d의 변동성을 일치 시킴(12.7)
# 배당이 없는(무배당) 유러피안 콜옵션의 1기간 이항모형
def Binomial_European_One_period(S, K, u, rf):
    d = 1/u
    t=1                                  # t = maturity
    n=1                                  # n 은 기간 : 1 period
    dt = t/n
    a = np.exp(rf * dt)                  # rf는 무위험 이자율
    df = 1/np.exp(rf * dt)               # df는 discount factor 할인계수
    prob = (a-d)/(u-d)
    
    cu = max(S*u - K, 0)                
    cd = max(S*d - K, 0)
    
    c = (prob*cu + (1-prob)*cd) * df
    return c

print(Binomial_European_One_period(S=100, K=100, u=1.1, rf=0.05)) 
 
S = np.linspace(0, 200, 1000)
Call_Value = np.zeros(len(S))

for i in range(len(S)):
    Call_Value[i] = Binomial_European_One_period(S=S[i], K=100, u=1.1, rf=0.05)

trace1 = go.Scatter(x=S, y=Call_Value)
data1=[trace1]
layout = go.Layout(width=800, height=400, xaxis=dict(title='Spot Price'), yaxis=dict(title='Option Value')) 
fig1 = dict(data=data1, layout=layout)
# fig1.write_image("Binomial_European_One_period.png")
iplot(fig1)