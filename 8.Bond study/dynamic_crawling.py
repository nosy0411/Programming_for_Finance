import pandas as pd
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('headless') # headless: 브라우저가 안뜸

driver = webdriver.Chrome("C:\\Users\hawoo\Desktop\FR_Study\FR-30th\Bond_study\FR_30_HWJ\chromedriver.exe", options=options)
URL="https://www.wsj.com/market-data/bonds"
driver.get(URL)

# class name을 이용한 방법
# class name이 매번 바뀌어서 이 방법은 못씀
# table_class_name = "WSJTables--table__body--3Y0p0d6H "
# table = driver.find_element_by_class_name(table_class_name)

# XPath를 이용한 방법
path = '//*[@id="root"]/div/div/div/div[2]/div[3]/div/div[3]/div[1]/div/table/tbody'
table = driver.find_element_by_xpath(path)

print(table.text)

# data를 dataframe로 변경한다.
rows=table.text.split('\n')
element=[]
for r in rows:
    element.append([i for i in r.split(' ')])
df=pd.DataFrame(element)
print('\n')
headers=['Maturity', 'Type','Coupon','Price Chg', 'Yield', 'Yield Chg']
df.columns=headers
df.iloc[:]=df.iloc[::-1].values

print(df)