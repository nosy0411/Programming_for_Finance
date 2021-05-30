import numpy as np
import scipy.stats as stats
from statsmodels.tsa.arima_process import arma_generate_sample
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix
from statsmodels.tsa.arima_model import ARIMA
import TaFeatureSet
import get_stock

# ARIMA(ar, d, ma) 모형으로 n개의 데이터를 샘플링한다


def sampleARIMA(ar, d, ma, n):
    arparams = np.array(ar)
    maparams = np.array(ma)
    ar = np.r_[1.0, -arparams]  # add zero-lag and negate
    ma = np.r_[1.0, maparams]  # add zero-lag

    # ARMA 모형으로 n개의 데이터를 샘플링한다
    y = arma_generate_sample(ar, ma, n)

    # 지정된 차분 횟수 (d) 만큼 누적한다
    for i in np.arange(d):
        y = np.cumsum(y)

    return y

# 시계열 데이터의 정규성을 확인한다


def checkNormality(data):
    fig = plt.figure(figsize=(10, 8))
    p1 = fig.add_subplot(2, 2, 1)
    p2 = fig.add_subplot(2, 2, 2)
    p3 = fig.add_subplot(2, 2, 3)
    p4 = fig.add_subplot(2, 2, 4)

    p1.plot(data)  # 육안으로 백색 잡음 형태인지 확인한다
    p1.set_title("Data")

    # Residual의 분포를 육안으로 확인한다
    r = np.copy(data)
    r.sort()
    pdf = stats.norm.pdf(r, np.mean(r), np.std(r))
    p2.plot(r, pdf)
    p2.hist(r, density=True, bins=100)
    p2.set_title("Distribution")

    # Q-Q plot을 그린다
    stats.probplot(data, dist="norm", plot=p3)

    # ACF plot을 확인한다. 백색 잡음은 자기상관성이 없다.
    plot_acf(data, lags=100, ax=p4)

    # Shapiro-Wilks 검정을 수행한다
    # (검정통계량, p-value)가 출력된다.
    # 귀무가설 : 정규분포 이다, 대립가설 : 아니다
    # p-value > 0.05 이면 귀무가설을 기각할 수 없다 --> "정규분포이다"
    w = stats.shapiro(data)
    print()
    print("Shapiro-Wilks 검정 : 검정통계량 = %.4f, p-value = %.4f" % (w[0], w[1]))


# Yahoo 사이트에서 주가 데이터를 수집하여 주가, 거래량, 수익률, MACD 지표를
# 관찰하고, 비정상 시계열 (Non-stationary)과 정상 시계열 (Stationary)의
# 차이점을 관찰한다.
# ----------------------------------------------------------------------

df = get_stock.getStockDataYahoo('069500.KS', start='2010-01-01')
df = pd.read_csv('StockData/069500.csv', index_col=0, parse_dates=True)

# 종가를 기준으로 일일 수익률을 계산한다.
df['Rtn'] = np.log(df['Close']) - np.log(df['Close'].shift(1))

# MACD 기술적 지표를 측정한다
df['macd'] = TaFeatureSet.MACD(df)
df = df.dropna()

# 주가, 거래량, 수익률, MACD를 그린다
fig = plt.figure(figsize=(10, 6))
p1 = fig.add_subplot(2, 2, 1)
p2 = fig.add_subplot(2, 2, 2)
p3 = fig.add_subplot(2, 2, 3)
p4 = fig.add_subplot(2, 2, 4)

p1.plot(df['Close'], color='blue', linewidth=1)
p2.plot(df['Volume'], color='red', linewidth=1)
p3.plot(df['Rtn'], color='purple', linewidth=1)
p4.plot(df['macd'], color='green', linewidth=1)
p1.set_title("Stock Price")
p2.set_title("Volume")
p3.set_title("Return")
p4.set_title("MACD oscilator")
p3.axhline(y=0, color='black', linewidth=1)
p4.axhline(y=0, color='black', linewidth=1)
plt.tight_layout()
plt.show()

# ARIMA 모형을 이용하여 주가을 예측해 본다.
# 예측 결과를 신뢰할 수 있는가? 없다면 그 원인은 무엇인가 ?
#
# ------------------------------------------------------

# Yahoo site에서 주가 데이터를 읽어온다
df = get_stock.getStockDataYahoo('000660.KS', start='2010-01-01')
p = pd.read_csv('StockData/000660.csv', index_col=0, parse_dates=True)

# 종가를 기준으로 일일 수익률을 계산한다.
p['Rtn'] = np.log(p['Close']) - np.log(p['Close'].shift(1))
p = p.dropna()

# 수익률 시계열을 육안으로 확인한다. 이분산성이 있는가?
plt.figure(figsize=(15, 10))
plt.plot(p['Rtn'], color='red', linewidth=1)
plt.show()

# 주가 데이터를 ARIMA(2,1,1) 모형으로 분석한다 (Fitting)
# int형이면 float형으로 변환한다
y = np.array(pd.to_numeric(p['Close'], downcast='float'))
model = ARIMA(y, order=(1, 1, 1))
model_fit = model.fit()
print(model_fit.summary())

# Fitting이 잘되었는지 확인하기 위해 Residual을 분석한다.
# Residual은 실제 데이터와 추정치의 차이이므로 백색 잡음 (잔차) 이어야 한다.
# 따라서 Residual은 정규분포 특성을 가져야한다. 정규분포 특성을 조사하면
# Fitting이 잘되었는지 확인할 수 있다.
residual = model_fit.resid
checkNormality(residual)  # 육안으로 백색 잡음 형태인지 확인한다

# 향후 10 기간 데이터를 예측한다
forecast = model_fit.forecast(steps=10)[0]
forecast = np.r_[y[-1], forecast]  # y의 마지막 값을 forecast 앞 부분에 넣는다

# 원 시계열과 예측된 시계열을 그린다
ytail = y[len(y)-100:]   # 뒷 부분 100개만 그린다
ax1 = np.arange(1, len(ytail) + 1)
ax2 = np.arange(len(ytail), len(ytail) + len(forecast))
plt.figure(figsize=(10, 6))
plt.plot(ax1, ytail, 'b-o', markersize=3, color='blue',
         label='Stock Price', linewidth=1)
plt.plot(ax2, forecast, color='red', label='Forecast')
plt.axvline(x=ax1[-1],  linestyle='dashed', linewidth=1)
plt.title("Time Series Forcast")
plt.legend()
plt.show()


# 시계열 공부 하면 해야할 것
# 정규분포 및 정규성 검정 (샤피로-월크) QQ plot
# 왜도, 첨도, 팻테일
# t-검정, F-검정
# 등분산 검정 (바틀렛 검증)
# 유동성 (ex. 롤 스프레드, 아미후드 비유동성, )
# 더빈-왓슨 : 자기 상관관계와 관련
# 잔차는 AR1 프로세스를 따른다는 대립가설에 대해 최소자승 회귀의 잔차는 자기상관을 따르지 않는다는 귀무가설을 검정하는 것
# 0-4 사이의 값을 가지며, 2에 가까울수록 자기상관관계가 없음
# AIC : 아카이케 정보 기준. 주어진 데이터에 대한 통계 모델의 상대적인 품질에 관한 척도
# BIC : 베이시언 정보 기준
# 쟈크 베라 검정 : 데이터가 정규 분포에 부합하는 왜도와 첨도를 갖는지 적합도를 테스트
# 귀무가설은 왜도가 0이라는 가설과 초과 점도가 0이라는 2개 가설이 합쳐진 결과
# 시계열 생성모형 ARIMA, GARCH ... 
