from bs4 import BeautifulSoup
import requests

response = requests.get("https://finance.naver.com/item/main.nhn?code=005930")
html = response.text
soup = BeautifulSoup(html, 'html5lib')
result = soup.find('table', {'class': 'tb_type1 tb_num'})
all_data = result.select('tr:nth-of-type(11) td')
all_result = []
for i in all_data:
    all_result.append(i.text)


print(all_result)
