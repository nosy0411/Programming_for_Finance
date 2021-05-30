import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup


tenors=['01M', '03M','06M','01Y','02Y','03Y','05Y','07Y','10Y','30Y']
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

for tenor in tenors:
    url = "https://www.wsj.com/market-data/quotes/bond/BX/TMUBMUSD" + tenor + "?mod=md_bond_overview_quote"
    req = requests.get(url,headers=headers)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')

    date = soup.select('span[id=quote_dateTime]')
    yield_data = soup.select('span[id=quote_val]')
    
    dt = datetime.datetime.strptime(date[0].text[-8:], "%m/%d/%y")
    print(date[0].text, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.year))