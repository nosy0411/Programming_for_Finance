import math
import numpy as np
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like


# Yahoo site로 부터 주가 데이터를 수집
def getStockDataYahoo(stockCode, start='', end=''):
    # 수집 기간
    if start == '':
        start = dt.datetime(2007, 1, 1)
    else:
        start = dt.datetime.strptime(start, '%Y-%m-%d')

    if end == '':
        end = dt.date.today()
    else:
        end = dt.datetime.strptime(end, '%Y-%m-%d')

    stock = pd.DataFrame()

    # Yahoo site로 부터 주가 데이터를 수집한다. 가끔 안들어올 때가 있어서 10번 시도한다.
    for i in range(0, 10):
        try:
            # 수정 주가로 환산하여 읽어온다
            stock = web.YahooDailyReader(
                stockCode, start, end, adjust_price=True).read()
        except:

            print("%s not collected (%d)" % (stockCode, i + 1))

        if not stock.empty:
            break

    if stock.empty:
        print("%s not collected" % stockCode)

    # 수정주가 비율은 이미 적용되었으므로 제거한다
    stock = stock.drop('Adj_Ratio', 1)

    # Volume이 0 인 경우가 있으므로, 이를 제거한다
    stock = stock.drop(stock[stock.Volume < 10].index)

    # 데이터에 NA 값이 있으면 제거한다
    stock = stock.dropna()

    # 수집한 데이터를 파일에 저장한다.
    stock.to_csv('StockData/' + stockCode[0:6] + '.csv', date_format='%Y-%m-%d')
    print("%s 데이터를 수집하였습니다. (rows = %d)" % (stockCode, len(stock)))
    return stock

# 지수이동평균을 계산한다
# data : Series


def EMA(data, n):
    ma = []
    # data 첫 부분에 na 가 있으면 skip한다
    x = 0
    while True:
        if math.isnan(data[x]):
            ma.append(data[x])
        else:
            break
        x += 1

    # x ~ n - 1 기간까지는 na를 assign 한다
    for i in range(x, x + n - 1):
        ma.append(np.nan)
    # x + n - 1 기간은 x ~ x + n - 1 까지의 평균을 적용한다
    sma = np.mean(data[x:(x + n)])
    ma.append(sma)

    # x + n 기간 부터는 EMA를 적용한다
    k = 2 / (n + 1)

    for i in range(x + n, len(data)):
        ma.append(ma[-1] + k * (data[i] - ma[-1]))

    return pd.Series(ma, index=data.index)


if __name__ == "__main__":
    stock = getStockDataYahoo("102110.KS")
    # today = dt.date.today()
    # stock['Close'].loc[today] = 26070
    print(EMA(stock['Close'], 90).values[-3:])
