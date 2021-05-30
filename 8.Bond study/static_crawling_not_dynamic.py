import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


url = "https://www.wsj.com/market-data/bonds"
req = requests.get(url,headers=headers)
html = req.text
soup = BeautifulSoup(html,'html.parser')
table = soup.find_all('tbody')
tr = table[0].select('tr')
print(tr)

# 바로 Libor금리가 나오는 것으로 보아 동적데이터는 뷰티풀숲으로 안가져와 지는 것 같다.