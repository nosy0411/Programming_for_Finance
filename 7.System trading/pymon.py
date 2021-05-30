import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame
import datetime
import yield_dividend
import numpy as np
import getstock

MARKET_KOSPI = 0
MARKET_KOSDAQ = 10


class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def is_it_float(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def run(self):
        buy_list = []
        num = len(self.kosdaq_codes)
        split_kosdaq_codes = self.kosdaq_codes[0:20]

        for i, code in enumerate(split_kosdaq_codes):
            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                buy_list.append(code)

        self.update_buy_list(buy_list)

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[]}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req","opt10081", 0, "0101")
        time.sleep(0.2)

        dog = DataFrame(self.kiwoom.ohlcv, columns=['open','high', 'low', 'close', 'volume'], index=self.kiwoom.ohlcv['date'])
        return dog

    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1<= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20/20
        if today_vol > avg_vol20*10:
            return True
        else:
            return False

    def update_buy_list(self, buy_list):
        f = open("buy_list.txt", "wt",encoding='UTF8')
        for code in buy_list:
            f.writelines("매수;%s;시장가;10;0;매수전\n" % (code))
        f.close()


    # 3년 동안의 국채시가배당률을 구하고, 최소량 최대 반환
    def get_min_max_divdiend_to_treasury(self, code):
        previous_dividend_yield = yield_dividend.get_previous_dividend_yield(code)
        three_years_treasury = yield_dividend.get_3years_treasury()
        today = datetime.datetime.now()
        curr_year = today.year
        previous_dividend_to_treasury = {}

        for year in range(curr_year-3, curr_year):
            if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
                if(self.is_it_float(previous_dividend_yield[year])):
                    ratio = float(
                        previous_dividend_yield[year])/float(three_years_treasury[year])
                else:
                    ratio = 0

                previous_dividend_to_treasury[year] = ratio

        min_ratio = min(previous_dividend_to_treasury.values())
        max_ratio = max(previous_dividend_to_treasury.values())

        return (min_ratio, max_ratio)

    def buy_check_by_dividend_algorithm(self,code): #위 함수에서 3년동안의 국채시가배당률 구하고 그 최댓값을 현재 국채시가배당률과 비교해서 매수
        estimated_dividend_to_treasury = yield_dividend.calculate_estimated_dividend_to_treasury(code)
        (min_ratio, max_ratio) = self.get_min_max_divdiend_to_treasury(code)

        if estimated_dividend_to_treasury>max_ratio:
            return (1,estimated_dividend_to_treasury)
        else:
            return (0,estimated_dividend_to_treasury)

    def run_dividend(self):
        buy_list=[]

        for code in self.kospi_codes:
            print("Check: ",code)
            ret = self.buy_check_by_dividend_algorithm(code)

            if ret[0]==1:
                print("Pass",ret)
                buy_list.append((code,ret[1]))
            else:
                print("Fail",ret)
    
    def run_trend(self,code,n):
        
        today = datetime.date.today()
        #현재가 받아오기
        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")

        code_format=str(code)+".KS"
        #야후에서 과거 데이터 가져오기
        stock=getstock.getStockDataYahoo(code_format)
        #과거 데이터 지수이동평균 계산
        ema_before = getstock.EMA(stock['Close'],n)

        #과거데이터에 현재가 추가
        stock['Close'].loc[today] = float(self.kiwoom.now_price)
        #현재가 포함시킨 지수이동평균 계산
        ema_after = getstock.EMA(stock['Close'],n)

        if ema_before.values[-3]>ema_before.values[-2] and ema_after.values[-2]<ema_after.values[-1]:
            print("3개월 지수이동평균 상승반전 상태입니다!")
            self.send_order(code)
            print("1주 매수가 완료되었습니다!")
        else:
            print("상승반전 상태가 아닙니다")
            #일단 상승반전 상태 아닌데 정상적으로 코드 돌아가는지 체크해야하니까 매수 코드 넣어봄
            self.send_order(code)
            print("상승반전 상태가 아니므로 1주만 구매했습니다.")

    def send_order(self,code_num):

        order_type_lookup={'신규매수':1,'신규매도':2, '매수취소':3, '매도취소':4}
        hoga_lookup = {'지정가':'00', '시장가':'03'}
        account_number = self.kiwoom.get_login_info("ACCNO")
        account = account_number.split(';')[0]
        print(account)
        order_type='신규매수'
        code = code_num
        hoga = '시장가'
        num = 1
        price = 0
        
        self.kiwoom.send_order("send_order_req","0101",account,order_type_lookup[order_type],code,num,price,hoga_lookup[hoga],"")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    # pymon.run_dividend()
    pymon.run_trend("102110",90)