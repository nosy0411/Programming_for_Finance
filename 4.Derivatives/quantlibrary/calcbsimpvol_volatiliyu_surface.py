import numpy as np 
from calcbsimpvol import calcbsimpvol
import QuantLib as ql
import math
import numpy as np
import pandas as pd

# 1년을 몇일로 볼것인가? 한국은 ACT 즉 실제 그 해의 일수 365로 고정한 것을 씀.
day_count = ql.Actual365Fixed() #Actual/365
calculation_date = ql.Date(30, 5, 2020)

T=[]
S=[]
K=[]
df = pd.read_csv("./123.csv")
for i in range(len(df)):
    # print(df['종목'][i][-5:])
    expiry=0
    if df['종목'][i][-9]=='0':
        if df['종목'][i][-7]=='6':
            expiry = ql.Date(11,6,2020)
        elif df['종목'][i][-7]=='7':
            expiry = ql.Date(9,7,2020)
        elif df['종목'][i][-7]=='8':
            expiry = ql.Date(13,8,2020)
        elif df['종목'][i][-7]=='9':
            expiry = ql.Date(10,9,2020)
        elif df['종목'][i][-8:-6]=='10':
            expiry = ql.Date(8,10,2020)
        elif df['종목'][i][-8:-6]=='11':
            expiry = ql.Date(12,11,2020)
        elif df['종목'][i][-8:-6]=='12':
            expiry = ql.Date(10,12,2020)
    elif df['종목'][i][-9]=='1':
        if df['종목'][i][-7]=='3':
            expiry = ql.Date(11,3,2021)
        elif df['종목'][i][-7]=='6':
            expiry = ql.Date(10,6,2021)
        elif df['종목'][i][-7]=='9':
            expiry = ql.Date(9,9,2021)
        elif df['종목'][i][-8:-6]=='12':
            expiry = ql.Date(9,12,2021)
    elif df['종목'][i][-9]=='2':
        if df['종목'][i][-7]=='3':
            expiry = ql.Date(10,3,2022)
        elif df['종목'][i][-7]=='6':
            expiry = ql.Date(9,6,2022)
        elif df['종목'][i][-7]=='9':
            expiry = ql.Date(8,9,2022)
        elif df['종목'][i][-8:-6]=='12':
            expiry = ql.Date(8,12,2022)

    T.append(round(day_count.yearFraction(calculation_date,expiry),4))
    K.append(float(df['종목'][i][-5:]))
    S.append(float(df['현재가'][i]))
print(T)
print(K)
print(S)
implied_volatility=[]

for i in range(len(df)):
    s = np.asarray(263.74) # Underlying Price : Kospi200 5.21
    k = np.asarray([K[i]]) # Strike Price 
    tau = np.asarray([T[i]]) # Time to Maturity 
    r = np.asarray(1.02)  # CD91일물 금리 2020.5.21일 기준
    q = np.asarray(0.00) # Dividend Rate 
    cp = np.asarray(-1) # Option Type 
    P = np.asarray([S[i]]) # Market Price
    
    imp_vol = calcbsimpvol(dict(cp=cp, P=P, S=s, K=k, tau=tau, r=r, q=q)) 
    implied_volatility.append(imp_vol[0][0])
print(implied_volatility)

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

trace = go.Surface(x=TM, y=KP, z=imp_vol, colorscale='Jet', opacity=0.8)
data = [trace] 
layout = go.Layout(title='Call Theta Surface', 
        scene={'xaxis':{'title':'Maturity'}, 'yaxis':{'title':'Spot Price'}, 'zaxis':{'title':'Theta'}}, 
        width=800, height=800, autosize=False, margin=dict(pad=0) ) 
fig = go.Figure(data=data, layout=layout) 
iplot(fig)