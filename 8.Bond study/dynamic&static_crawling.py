import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument('headless') # headless: 브라우저가 안뜸

driver = webdriver.Chrome('C:\\Users\\inventor\\Desktop\\FR study\\FR-30th\\Bond_study\\FR_30_NIH\\chromedriver.exe', options=options)
URL="https://www.wsj.com/market-data/bonds/treasuries"
driver.get(URL)

source = driver.page_source
tbonds_code = BeautifulSoup(source,'html.parser')

#xpath을 이용한 방법
button_xpath = '//*[@id="root"]/div/div/div/div[2]/div/div/div[3]/ul/li[2]/button'
button = driver.find_element_by_xpath(button_xpath)
button.click()

source = driver.page_source
tbills_code = BeautifulSoup(source,'html.parser')

#date 가져오기 
date = tbonds_code.select('div > div > div > div > div > div > div > div > h3 > span')
data = date[1].text
print(data)

#tbond table 가져오기
tbond_rows = tbonds_code.select('div > div > div > div > div > div > div > div > table > tbody > tr')
# print(tbond_rows)

#tbill table 가져오기
tbill_rows = tbills_code.select('div > div > div > div > div > div > div > div > table > tbody > tr')
# print(tbill_rows)

tbond_content = []
tbond_contents = []

for tbond_row in tbond_rows:
    tds = tbond_row.find_all("td")
    for td in tds:
        tbond_content.append(td.text)
    tbond_contents.append(tbond_content)
    tbond_content=[]

tbond_df=pd.DataFrame(tbond_contents)
tbond_headers=['Maturity', 'Coupon','Bid','Ask','Chg', 'Asked Yield']
tbond_df.columns=tbond_headers
tbond_df.set_index('Maturity',inplace=True)


tbill_content = []
tbill_contents = []

for tbill_row in tbill_rows:
    tds = tbill_row.find_all("td")
    for td in tds:
        tbill_content.append(td.text)
    tbill_contents.append(tbill_content)
    tbill_content=[]

tbill_df=pd.DataFrame(tbill_contents)
tbill_headers=['Maturity','Bid','Ask','Chg', 'Asked Yield']
tbill_df.columns=tbill_headers
tbill_df.set_index('Maturity',inplace=True)

print(tbond_df.head(10))
print(tbill_df.head())