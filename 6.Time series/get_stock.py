import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import TaFeatureSet
import os
pd.core.common.is_list_like = pd.api.types.is_list_like

path = r'C:\Users\inventor\Desktop\FR study\FR-30th\Stock_study\FR_30_NIH\TimeSeriesProject'
os.chdir(path)


# Yahoo site로 부터 주가 데이터를 수집
def Get_Stock_Data_Yahoo(Stock_Code, start='', end=''):
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
            stock = web.YahooDailyReader(Stock_Code, start, end,
                                         adjust_price=True).read()

        except Exception:

            print("%s not collected (%d)" % (Stock_Code, i + 1))

        if not stock.empty:
            break

    if stock.empty:
        print("%s not collected" % Stock_Code)

    # 수정주가 비율은 이미 적용되었으므로 제거한다
    stock = stock.drop('Adj_Ratio', 1)

    # Volume이 0 인 경우가 있으므로, 이를 제거한다
    stock = stock.drop(stock[stock.Volume < 10].index)

    # 데이터에 NA 값이 있으면 제거한다
    stock = stock.dropna()

    # 수집한 데이터를 파일에 저장한다.
    stock.to_csv('StockData/' + Stock_Code[0:6]
                 + '.csv', date_format='%Y-%m-%d')
    print("%s 데이터를 수집하였습니다. (rows = %d)" % (Stock_Code, len(stock)))
    return stock


# 일일 데이터를 주간 (Weekly), 혹은 월간 (Monthly)으로 변환한다
def myAgg(x):
    names = {'Open': x['Open'].head(1),
             'High': x['High'].max(),
             'Low': x['Low'].min(),
             'Close': x['Close'].tail(1),
             'Volume': x['Volume'].mean()}

    return pd.Series(names, index=['Open', 'High', 'Low', 'Close', 'Volume'])


def Get_Week_Month_Ohlcv(x, datetype='Week'):

    if datetype == 'Week':
        rtn = x.resample('W-Fri').apply(myAgg)
    elif datetype == 'Month':
        rtn = x.resample('M').apply(myAgg)
    else:
        print("invalid type in getWeekMonthOHLC()")
        return
    rtn = rtn.dropna()
    rtn = rtn.apply(pd.to_numeric)
    return rtn


if __name__ == "__main__":
    # Tiger 200 etf
    stock = Get_Stock_Data_Yahoo("102110.KS")
    # today = dt.date.today()
    # stock['Close'].loc[today] = 26070
    print(TaFeatureSet.EMA(stock['Close'], 90).values[-3:])
