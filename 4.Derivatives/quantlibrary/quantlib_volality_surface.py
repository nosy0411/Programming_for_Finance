import QuantLib as ql
import math
import numpy as np

# 1년을 몇일로 볼것인가? 한국은 ACT 즉 실제 그 해의 일수 365로 고정한 것을 씀.

day_count = ql.Actual365Fixed() #Actual/365
SeoulCalendar = ql.SouthKorea()

calculation_date = ql.Date(6, 10, 2020)
ql.Settings.instance().evaluationDate = calculation_date

# Simple Quote Objects, # QuoteHandle클래스
dividend_yield = ql.QuoteHandle(ql.SimpleQuote(0.0))

risk_free_rate = 1.02 # CD91일물 금리 2020.5.21일 기준
dividend_rate = 0.0


plot_strikes = np.arange(160.0, 365, 2.5)
