import math
import numpy as np
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like

# Z-score normalization
def scale(data):
    col = data.columns[0]
    return (data[col] - data[col].mean()) / data[col].std()

# 전일 Close price와 금일 Close price를 이용하여 변동성을 계산한다
def CloseVol(ohlc, n):
    rtn = pd.DataFrame(ohlc['Close']).apply(lambda x: np.log(x) - np.log(x.shift(1)))
    vol = pd.DataFrame(rtn).rolling(window=n).std()

    return pd.DataFrame(vol, index=ohlc.index)

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
    # stock.to_csv('StockData/' + stockCode[0:6] + '.csv', date_format='%Y-%m-%d')
    print("%s 데이터를 수집하였습니다. (rows = %d)" % (stockCode, len(stock)))
    return stock

if __name__ == "__main__":
    stock = getStockDataYahoo("^KS200")
    fvol = scale(CloseVol(stock, 90))
    ft = pd.DataFrame()
    ft['volatility'] = fvol
    ft = ft.dropna()
    