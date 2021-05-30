import pandas_datareader as web
import datetime

start = datetime.datetime(2010, 1, 1)

end = datetime.datetime(2020, 7, 8)

Aaa = web.DataReader('DAAA', 'fred', start, end)

Baa = web.DataReader('DBAA', 'fred', start, end)

print(Aaa)
print(Baa)