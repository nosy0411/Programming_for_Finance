from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import datetime
import matplotlib
import matplotlib.pyplot as plt
import json
 
 
if __name__ == "__main__":

    # 한국은행API 인증코드
    key = '19EOI9YS8C4QP7FVB88R'
 
    # https://ecos.bok.or.kr/jsp/openapi/OpenApiController.jsp?t=guideServiceDtl&apiCode=OA-1040&menuGroup=MENU000004
    # 여기서 주소 만들면 쉽다.
    url="http://ecos.bok.or.kr/api/StatisticSearch/"+key+"/json/kr/1/10000/060Y001/DD/190001/202008/010190000/?/?/"

    result = urlopen(url)
    print(result)
    html = result.read()
    data = json.loads(html)
    # print(data)
    data=data["StatisticSearch"]["row"]
    Interest_rate = pd.DataFrame(data)
    Interest_rate = Interest_rate[Interest_rate["ITEM_CODE1"]=="010190000"]
    Interest_rate["DATA_VALUE"]=Interest_rate["DATA_VALUE"].astype("float")
    # print(Interest_rate)
    Interest_rate["DATA_VALUE"].plot()
    plt.show()
 
    Interest_rate["TIME"] = Interest_rate["TIME"].astype("str")
 
    Interest_rate["TIME"] = Interest_rate["TIME"].apply(lambda x : datetime.datetime.strptime(x, '%Y%m%d'))
    # print(Interest_rate["TIME"])
    
    # remove duplicates
    xlabel = Interest_rate["TIME"]
    xlabel = xlabel.drop_duplicates()
    
    Interest_rate=Interest_rate.sort_values("TIME")
    Interest_rate.set_index("TIME",inplace=True)
    # print(Interest_rate)
 
    # x축. y축 설정
    plt.scatter(Interest_rate.index,Interest_rate["DATA_VALUE"])
    plt.plot(Interest_rate.index,Interest_rate["DATA_VALUE"])
    plt.xticks(Interest_rate.index, xlabel,rotation=70)
    # plt.show()
