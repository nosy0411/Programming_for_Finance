import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

tenors=['01M', '03M','06M','01Y','02Y','03Y','05Y','07Y','10Y','30Y']

maturities=[]
yields=[]
coupons=[]

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

for tenor in tenors:
    url = "https://www.wsj.com/market-data/quotes/bond/BX/TMUBMUSD" + tenor + "?mod=md_bond_overview_quote"
    req = requests.get(url,headers=headers)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    
    # 원하는 정보가 있는 위치 찾기 

    # soup.select('원하는 정보')  # select('원하는 정보') -->  단 하나만 있더라도, 복수 가능한 형태로 되어있음

    # soup.select('태그명')
    # soup.select('.클래스명')
    # soup.select('상위태그명 > 하위태그명 > 하위태그명')
    # soup.select('상위태그명.클래스명 > 하위태그명.클래스명')    # 바로 아래의(자식) 태그를 선택시에는 > 기호를 사용
    # soup.select('상위태그명.클래스명 하~위태그명')              # 아래의(자손) 태그를 선택시에는   띄어쓰기 사용
    # soup.select('상위태그명 > 바로아래태그명 하~위태그명')     
    # soup.select('.클래스명')
    # soup.select('#아이디명')                  # 태그는 여러개에 사용 가능하나 아이디는 한번만 사용 가능함! ==> 선택하기 좋음
    # soup.select('태그명.클래스명)
    # soup.select('#아이디명 > 태그명.클래스명)
    # soup.select('태그명[속성1=값1]')

    yield_data = soup.select('span[id=quote_val]') # yield data
    # yield_data = soup.select('body > div > div > section > div > div > div > ul > li > span > span') # yield data
    # print(type(yield_data))
    # print(type(yield_data[0]))

    # coupon_and_maturity = soup.select('body > div > div > section > div > div > div > ul > li > div > span') # coupon rate & maturity date
    coupon_and_maturity = soup.select('span[class=data_data]') # coupon rate & maturity date
    # print(coupon_and_maturity)

    ytm = yield_data[0].text
    coupon = coupon_and_maturity[2].text
    maturity = coupon_and_maturity[3].text
    
    ytm = float(ytm[:-1])
    
    if coupon!='':
        coupon = float(coupon[:-1])
    else:
        coupon=0.0
    
    maturity_revise = datetime.datetime.strptime(maturity, '%m/%d/%y')
    yields.append(ytm)
    coupons.append(coupon)
    maturities.append(maturity_revise)

df = pd.DataFrame([maturities, yields, coupons]).transpose()
headers=['maturity','yield','coupon']
df.columns = headers
df.set_index('maturity',inplace=True)

print(df)