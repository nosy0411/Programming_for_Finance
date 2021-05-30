import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

tenors=['01M', '03M','06M','01Y','02Y','03Y','05Y','07Y','10Y','30Y']
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
bond_headers=['Date', 'Open','High','Low','Close']
bond_table_list=[]

for i, tenor in enumerate(tenors):

    url1 = "https://www.wsj.com/market-data/quotes/bond/BX/TMUBMUSD" + tenor + "?mod=md_bond_overview_quote"
    req = requests.get(url1,headers=headers)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')

    date = soup.select('span[id=quote_dateTime]')
    yield_data = soup.select('span[id=quote_val]')

    dt = datetime.datetime.strptime(date[0].text[-8:], "%m/%d/%y")

    # print(date[0].text)
    month=str(dt.month).zfill(2)
    day=str(dt.day).zfill(2)
    year=str(dt.year)

    url2='https://www.wsj.com/market-data/quotes/ajax/historicalpricesbond/8/'\
        'TMUBMUSD'+tenor+'?MOD_VIEW=page&ticker=TMUBMUSD'+tenor+'&country=BX&exchange=XTUP'\
        '&instrumentType=BOND&num_rows=20000&range_days=20000&startDate=03%2F01%2F2006&endDate='+month+'%2F'+day+'%2F'+year
    req = requests.get(url2,headers=headers)
    html = req.text
    historical_price = BeautifulSoup(html,'html.parser')

    bond_table =  historical_price.find_all('tbody')
    bond_rows = bond_table[0].select('tr')

    bond_content = []
    bond_contents = []

    for bond_row in bond_rows:
        tds = bond_row.find_all("td")
        for td in tds:
            bond_content.append(td.text)
        bond_content[0]=datetime.datetime.strptime(bond_content[0],"%m/%d/%y")
        bond_contents.append(bond_content)
        bond_content=[]

    bond_df=pd.DataFrame(bond_contents)
    bond_df.columns=bond_headers
    bond_df.set_index('Date',inplace=True)

    bond_table_list.append(bond_df)
    # print(bond_table_list[i].head(5))
    # print('\n\n\n')

# print(bond_table_list[0])
