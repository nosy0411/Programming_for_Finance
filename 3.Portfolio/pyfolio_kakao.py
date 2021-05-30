import FinanceDataReader as fdr
import pyfolio as pf

df = fdr.DataReader('035720', '1995-01-01')

print(df.head(10))
# return_series = df['Close'].pct_change().fillna(0)

# pf.create_returns_tear_sheet(return_series)