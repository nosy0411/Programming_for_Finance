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

# 연결재무제표 데이터프레임 형태로 만들어 주기
def make_fs_dataframe(firm_code):
    # fs_url = "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode="+firmcode
    fs_url=f"http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode={firm_code}"
    driver.get(fs_url)

    fs_page = driver.page_source
    fs_tables = pd.read_html(fs_page)
    # print(len(fs_tables))
    # 여러개 버튼을 클릭하고 싶을 때 element -> elements
    # buttons = driver.find_elements_by_xpath('//*[@class="btn_acdopen"]')
    # 이 방법은 안됨 ㅜ

    for i in range(len(fs_tables)):
        # table과 grid 번호가 안맞는 문제가 있음
        # for j in range(len(fs_tables[i])):
        for j in range(20):
            try :
                driver.find_element_by_xpath(f'//*[@id="grid{i+1}_{j+1}"]').click()

            except NoSuchElementException :
                continue

    fs_page = driver.page_source
    fs_tables = pd.read_html(fs_page)

    # 포괄손익계산서 Income statement IS
    fs_is = fs_tables[0]

    # 전년, 분기는 계산할 수 있으므로 4개년치만 가져온다
    # fs_is = fs_is.set_index('IFRS(연결)')
    # fs_is = fs_is[fs_is.columns[:4]]

    # 인덱스 이름(계정목록들)을 지정해주고 빼주기. 첫째 열이 IFRS(연결), IFRS(개별), GAAP(개별)과 같이 상황에 따라 다름
    first_column=fs_is.columns[0]
    fs_is.index=fs_is[first_column].values
    # inplace는 변수 대입 안해줘도 되고 axis=1은 열기준
    fs_is.drop([first_column,'전년동기','전년동기(%)'], inplace=True, axis=1)


    # 행 목록 필요없는 부분 제거
    for i, name in enumerate(fs_is.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_is.rename(index={str(fs_is.index[i]):str(name)}, inplace=True)

    # 포괄손익계산서 Income statement IS중 원하는 계정만 가져온다. 기준을 정하고 만들어보자
    # fs_is = fs_is.iloc[['매출액', '영업이익', '판매비와관리비', '당기순이익']]
    
    # 재무상태표 Balance Sheet BS
    fs_bs = fs_tables[2]

    # 인덱스 이름(계정목록들)을 지정해주고 빼주기. 첫째 열이 IFRS(연결), IFRS(개별), GAAP(개별)과 같이 상황에 따라 다름
    first_column=fs_bs.columns[0]
    fs_bs.index=fs_bs[first_column].values
    # inplace는 변수 대입 안해줘도 되고 axis=1은 열기준
    fs_bs.drop([first_column], inplace=True, axis=1)

    for i, name in enumerate(fs_bs.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_bs.rename(index={str(fs_bs.index[i]):str(name)}, inplace=True)

    # 현금흐름표 statement of cash flow CF
    fs_cf = fs_tables[4]

    # 인덱스 이름(계정목록들)을 지정해주고 빼주기. 첫째 열이 IFRS(연결), IFRS(개별), GAAP(개별)과 같이 상황에 따라 다름
    first_column=fs_cf.columns[0]
    fs_cf.index=fs_cf[first_column].values
    # inplace는 변수 대입 안해줘도 되고 axis=1은 열기준
    fs_cf.drop([first_column], inplace=True, axis=1)

    for i, name in enumerate(fs_cf.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_cf.rename(index={str(fs_cf.index[i]):str(name)}, inplace=True)

    fs_df=pd.concat([fs_is,fs_bs,fs_cf])

    return fs_df

# 증권 종목쪽 데이터는 재무내용이 달라서 ElementNotInteractableException 에러 떠서 따로 만듬
def er_fs_dataframe(firm_code):

    fs_url=f"http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode={firm_code}"
    driver.get(fs_url)

    fs_page = driver.page_source
    fs_tables = pd.read_html(fs_page)

    for i in range(len(fs_tables)):
        for j in range(45):
            # print(i, j)
            try :
                driver.find_element_by_xpath(f'//*[@id="grid{i+1}_{j+1}"]').click()

            except NoSuchElementException :
                continue
            except ElementNotInteractableException:
                try:
                    print('wait...click')
                    element = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="grid{i+1}_{j+1}"]')))
                    element.click()
                    print('click ok')
                except TimeoutException:
                    print("timeout")
                    continue

    fs_page = driver.page_source
    fs_tables = pd.read_html(fs_page)

    fs_is = fs_tables[0]

    first_column=fs_is.columns[0]
    fs_is.index=fs_is[first_column].values
    fs_is.drop([first_column,'전년동기','전년동기(%)'], inplace=True, axis=1)


    for i, name in enumerate(fs_is.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_is.rename(index={str(fs_is.index[i]):str(name)}, inplace=True)


    fs_bs = fs_tables[2]

    first_column=fs_bs.columns[0]
    fs_bs.index=fs_bs[first_column].values
    fs_bs.drop([first_column], inplace=True, axis=1)

    for i, name in enumerate(fs_bs.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_bs.rename(index={str(fs_bs.index[i]):str(name)}, inplace=True)

    fs_cf = fs_tables[4]

    first_column=fs_cf.columns[0]
    fs_cf.index=fs_cf[first_column].values
    fs_cf.drop([first_column], inplace=True, axis=1)

    for i, name in enumerate(fs_cf.index):
        if '참여한' in name:
            name = '*'+name.strip().replace('계산에 참여한 계정 감추기','')
            fs_cf.rename(index={str(fs_cf.index[i]):str(name)}, inplace=True)

    fs_df=pd.concat([fs_is,fs_bs,fs_cf])

    return fs_df


# SQLite3 DB 불러오기
con = sqlite3.connect("상장법인목록.db")
code_data = pd.read_sql("SELECT * FROM CorpList", con)
con.close()

code_data = code_data[['종목코드', '기업명']]


# 재무제표 SQLite3 DB로 저장하기
con = sqlite3.connect("재무제표정보.db")

for i, code in enumerate(code_data['종목코드']):

    code='A'+str(code)

    try:
        fs_data = make_fs_dataframe(code)
        fs_data.to_sql(code, con, if_exists="replace", index=True)

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
        print(code + "not interactable")
        fs_data = er_fs_dataframe(code)
        fs_data.to_sql(code, con, if_exists="replace", index=True)
        continue

con.close()