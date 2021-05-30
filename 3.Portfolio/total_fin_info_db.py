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
import FS_info_db, FR_info_db, Invest_index_info_db

options = webdriver.ChromeOptions()
options.add_argument('headless') # headless: 브라우저가 안뜸
driver = webdriver.Chrome('C:\\Users\\inventor\\Desktop\\FR study\\FR-30th\\Bond_study\\FR_30_NIH\\chromedriver.exe', options=options)

# 데이터프레임 형태 바꿔주기
def change_df(firm_code, dataframe):
    for num, col in enumerate(dataframe.columns):
        temp_df = pd.DataFrame({firm_code : dataframe[col]})
        temp_df = temp_df.T
        temp_df.columns = [[col]*len(dataframe), temp_df.columns]
        if num == 0:
            total_df = temp_df
        else:
            total_df = pd.merge(total_df, temp_df, how='outer', left_index=True, right_index=True)    
    
    return total_df


# SQLite3 DB 불러오기
con = sqlite3.connect("상장법인목록.db")
code_data = pd.read_sql("SELECT * FROM CorpList", con)
con.close()

code_data = code_data[['종목코드', '기업명']]

# 제무데이터 한방에 정리 SQLite3 DB로 저장하기
con = sqlite3.connect("통합재무데이터.db")

for i, code in enumerate(code_data['종목코드']):

    try : 
        code='A'+str(code)

        fs_df = FS_info_db.make_fs_dataframe(code)
        transform_fs = change_df(code,fs_df)
        transform_fs.to_sql('재무제표', con, if_exists="append", index=True)

        fr_df = FR_info_db.make_fr_dataframe(code)
        transform_fr = change_df(code,fr_df)
        transform_fr.to_sql('재무비율', con, if_exists="append", index=True)

        invest_df = Invest_index_info_db.make_invest_dataframe(code)
        transform_invest = change_df(code,invest_df)
        transform_invest.to_sql('투자지표', con, if_exists="append", index=True)
    
    except ValueError:
        print("temporary error")
        print(code + " Value error")
        continue

    except ImportError:
        print("temporary error")
        print(code + " Import error")
        continue
    # 이상한 종목 ex. 094800 맵스리얼티1 168490 한국패러랠 같은 종목은 fnguide에 정보가 없어서 함수에서 오류가 남 (전년동기, %)
    except KeyError:
        print("temporary error")
        print(code + " key error")
        continue

    # 위 keyerror랑 같은 문제인데 함수를 어떻게 짰냐에 따라 type error도 남 (참여한 부분)
    except TypeError:
        print("temporary error")
        print(code + " Type error")
        continue
    
    # 증권주들은 통합 재무 데이터를 구성할때 열 목록들이 다르므로 추가해주지 않음 
    except ElementNotInteractableException:
        print(code + " not interactable")
        continue

con.close()