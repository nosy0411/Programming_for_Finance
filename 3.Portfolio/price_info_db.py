import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import datetime


# SQLite3 DB 불러오기
con = sqlite3.connect("상장법인목록.db")
code_data = pd.read_sql("SELECT * FROM CorpList", con)
con.close()

code_data = code_data[['종목코드', '기업명']]

# print(code_data['종목코드'])

def func_price_dataframe(code, day, count):
    url = f'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe={day}&count={count}&requestType=0'

    xml_data = requests.get(url)
    soup_xml = BeautifulSoup(xml_data.text, 'lxml')
    
    price_table=[]

    for i, row in enumerate(soup_xml.find_all('item')):
        price = row['data'].split('|')
        
        if price[0] >= "20000101":  
            price[0] = datetime.datetime.strptime(price[0],'%Y%m%d')
            price[1] = int(price[1]) 
            price[2] = int(price[2]) 
            price[3] = int(price[3]) 
            price[4] = int(price[4]) 
            price[5] = int(price[5]) 
            price_table.append(price)

    price_df=pd.DataFrame(price_table)
    price_headers=['Date', 'Open','High','Low','Close', 'Volume']
    price_df.columns=price_headers
    price_df.set_index('Date',inplace=True)

    return price_df


# SQLite3 DB로 저장하기
con = sqlite3.connect("종목가격정보.db")

for i, code in enumerate(code_data['종목코드']):
    price_data = func_price_dataframe(code, 'day', '6000')

    price_data.to_sql(code, con, if_exists="replace", index=True)

con.close()