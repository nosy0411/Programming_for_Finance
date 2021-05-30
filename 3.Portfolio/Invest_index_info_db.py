import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
import time
import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless') # headless: 브라우저가 안뜸
driver = webdriver.Chrome('C:\\Users\\inventor\\Desktop\\FR study\\FR-30th\\Bond_study\\FR_30_NIH\\chromedriver.exe', options=options)

# 투자지표 데이터프레임 형태로 만들어 주기
def make_invest_dataframe(firm_code):
    invest_url=f"http://comp.fnguide.com/SVO2/ASP/SVD_invest.asp?pGB=3&gicode={firm_code}"
    driver.get(invest_url)

    invest_page = driver.page_source
    invest_tables = pd.read_html(invest_page)

    for i in range(15):

        try :
            driver.find_element_by_xpath(f'//*[@id="grid{1}_{i}"]').click()

        except NoSuchElementException :
            continue
        except ElementNotInteractableException:
            try:
                print('wait...click')
                element = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="grid{1}_{i}"]')))
                element.click()
                print('click ok')
            except TimeoutException:
                print("timeout")
                continue

    invest_page = driver.page_source
    invest_tables = pd.read_html(invest_page)

    invest_df = invest_tables[1]

    # 인덱스 이름(계정목록들)을 지정해주고 빼주기. 첫째 열이 IFRS(연결), IFRS(개별), GAAP(개별)과 같이 상황에 따라 다름
    first_column=invest_df.columns[0]
    invest_df.index=invest_df[first_column].values
    invest_df.drop([first_column], inplace=True, axis=1)

    # 행 목록 필요없는 부분 제거
    for i, name in enumerate(invest_df.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            invest_df.rename(index={str(invest_df.index[i]):str(name)}, inplace=True)

    return invest_df

# SQLite3 DB 불러오기
con = sqlite3.connect("상장법인목록.db")
code_data = pd.read_sql("SELECT * FROM CorpList", con)
con.close()

code_data = code_data[['종목코드', '기업명']]

# 투자지표 SQLite3 DB로 저장하기
con = sqlite3.connect("투자지표정보.db")

for i, code in enumerate(code_data['종목코드']):

    try:
        code='A'+str(code)
        invest_data = make_invest_dataframe(code)
        invest_data.to_sql(code, con, if_exists="replace", index=True)
    
    except ValueError:
        print("temporary error")
        print(code + " Value error")
        continue

    # 투자회사 종목 096300 가 이 에러가 나옴. fnguide상으로는 안내페이지 나옴
    except ImportError:
        print("temporary error")
        print(code + " Import error")
        continue
    
    # 이상한 종목 ex. 094800 맵스리얼티1 168490 한국패러랠 같은 종목은 fnguide에 정보가 없어서(안내페이지 x) 함수에서 오류가 남 (전년동기, %)
    except KeyError:
        print("temporary error")
        print(code + " key error")
        continue

    # 위 keyerror랑 같은 문제인데 함수를 어떻게 짰냐에 따라 type error도 남 (참여한 부분)
    except TypeError:
        print("temporary error")
        print(code + " Type error")
        continue
    except ElementNotInteractableException:
        continue

con.close()