import pandas_datareader.data as pdr
import yfinance as yf
yf.pdr_override()
from pandas.tseries.offsets import Day, MonthEnd
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy.stats import rankdata

# 글로벌 자산배분에 많이 사용되는 대표적인 10개 자산군
# (1) 미국 주식 / (2) 유럽 주식 / (3) 일본 주식 / (4) 이머징 주식 (5) 미 장기채 
# (6) 미 중기채 / (7) 미국 리츠 / (8) 글로벌 리츠 (9) 금 / (10) 상품

# 자산배분의 방법 
# 1) 주식과 채권 외에 상관관계가 낮은 자산군을 추가하여 분산 투자 (전략적 자산배분: Strategic Asset Allocation, SAA)
# 2) 미래 수익률과 변동성을 추정하여 자산 간 비중 조절 (전술적 자산배분: Tactical Asset Allocation, TAA)

tickers = ['SPY', 'IEV', 'EWJ', 'EEM', 'TLT', 'IEF', 'IYR', 'RWX', 'GLD', 'DBC']
start = '2007-12-30'

# SPY : SPDR S&P 500 (SPY)
# IEV : iShares Europe ETF (IEV)
# EWJ : iShares MSCI Japan ETF (EWJ)
# EEM : iShares MSCI Emerging Markets Indx (EEM)
# TLT : iShares Barclays 20+ Yr Treas.Bond (TLT)
# IEF : iShares Barclays 7-10 Year Trasry Bnd Fd (IEF)
# IYR : iShares US Real Estate ETF (IYR)
# RWX : SPDR Dow Jones Interntnl Real Estate ETF (RWX)
# GLD : SPDR Gold Shares (GLD)
# DBC : PowerShares DB Com Indx Trckng Fund (DBC)


all_data = {}
for ticker in tickers:
    all_data[ticker] = pdr.get_data_yahoo(tickers, start)

# 딕셔너리에서 data중 수정주가부분만 갖고오고 그 중에 해당 티커만 데이터를 가져온다.
prices = pd.DataFrame({tic : data['Adj Close'][tic] for tic, data in all_data.items()})
prices = prices.fillna(method = 'ffill')
rets = prices.pct_change(1)

# 거래비용 (수익률 차이)
fee = 0.0030
# n 개월 모멘텀
lookback = 12
# 상위 n개 종목
num = 5

# 월말 기준이 되는 지점 찾기
s = pd.Series(np.arange(prices.shape[0]), index=prices.index)
ep = s.resample("M", how="max")