import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from functools import reduce

matplotlib.use('TkAgg')  #  'Agg' or 'Qt5Agg'

def api_fetch(demo_url):
    #demo_url=f'https://eodhd.com/api/eod/AAPL.US?from=2024-01-01&period=d&api_token=DEMO&fmt=json'
        try:
            response=requests.get(demo_url)
            response.raise_for_status()
            data=response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {e}')
            return None
pekabex=api_fetch(f'https://eodhd.com/api/eod/PBX.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
wig20=api_fetch(f'https://eodhd.com/api/eod/ETFBW20TR.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
nasdaq100=api_fetch(f'https://eodhd.com/api/eod/CNDX.AS?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
def opening(file):
    """fetching from notebook as json type for tests"""
    with open(f'{file}', 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            data = json.loads(content)
            print(data)
            return data
        except json.JSONDecodeError as e:
            print("Bład parsowania JSON: ", e)
        print(type(data))
#pekabex=opening('API Pekabex.txt')
#wig20=opening('etfbw20TR.WAR.txt')

#print(pekabex)
#print(type(pekabex))

def to_df(df):
    ndf=pd.DataFrame(df)
    ndf = ndf.drop('warning', axis=1, errors='ignore')  # required to specify row=-0 or column=1
    return ndf
pekabex=to_df(pekabex)
wig20=to_df(wig20)
nasdaq100=to_df(nasdaq100)
"""
pekabex.plot(x='date', y='close')
wig20.plot(x='date', y='close')
plt.show()
"""
def portfolio_quartelly(): #all records by/sell for quarter portfolio
    """Zwraca DataFrame z historią transakcji (kupna/sprzedaży)."""
    pkbd = [{'date': '2024-03-06', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex', 'currency':'PLN'},
            {'date': '2024-03-29', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex', 'currency':'PLN'},
            {'date': '2024-04-23', 'volume': 4, 'operation': 'sell', 'ticker': 'pekabex', 'currency':'PLN'}]
    wig20d = [{'date': '2024-12-09', 'volume': 11.3675, 'operation': 'buy', 'ticker': 'wig20', 'currency':'PLN'}]
    nasdaq100=[{'date': '2024-12-09', 'volume': 0.0898, 'operation': 'buy', 'ticker': 'nasdaq100', 'currency':'USD'}]
    china=[{'date': '2024-12-09', 'volume': 15.809, 'operation': 'buy', 'ticker': 'msci china', 'currency':'USD'}]
    mwig40=[{'date': '2024-01-08', 'volume': 1, 'operation': 'buy', 'ticker': 'mwig40', 'currency':'PLN'},
            {'date': '2024-03-14', 'volume': 1, 'operation': 'buy', 'ticker': 'mwig40', 'currency':'PLN'}]
    artificial_intelligence=[{'date': '2025-01-23', 'volume': 0.337, 'operation': 'buy', 'ticker': 'AI', 'currency':'USD'}]
    semiconductor=[{'date': '2024-12-09', 'volume': 1, 'operation': 'buy', 'ticker': 'semiconductors', 'currency':'USD'}]
    digitalisation=[{'date': '2024-01-08', 'volume': 1, 'operation': 'buy', 'ticker': 'digitalisation', 'currency':'USD'},
                    {'date': '2024-04-02', 'volume': 1, 'operation': 'buy', 'ticker': 'digitalisation', 'currency':'USD'}]
    uranium_miners=[{'date': '2024-12-09', 'volume': 2.8277, 'operation': 'buy', 'ticker': 'uranium miners', 'currency':'USD'}]
    df_combined = pd.DataFrame(pkbd+wig20d+nasdaq100+china+mwig40+artificial_intelligence+semiconductor+digitalisation+uranium_miners)
    return df_combined
transakcje=portfolio_quartelly()
print(transakcje)

def portfolio_conn():
    """ portoflio Dataframe, changes value for sell operations, adds new column with cumulative sum of shares volume"""
    connector=transakcje
    connector['volume']=connector.apply(lambda row: row['volume'] if row['operation']=='buy' else -row['volume'], axis=1) # trying to compare an entire Series (connector['operation']) to a single value ('buy') within the lambda function. To fix this, we need to modify the lambda function to operate on individual rows. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
    #connector['sum_on_date']=connector['volume'].cumsum() #it sums rows conecutively
    connector['sum_on_date'] = connector.groupby('ticker')['volume'].cumsum()
    return connector
print(portfolio_conn())
"""
    my=pd.DataFrame(columns=['date','close','volume'])
    my['close']=pekabex['close']+wig20['close']
    my['date']=pekabex['date']
    #my=pd.merge([])
    print(my.head())
    my.plot(x='date', y='close')
    plt.show()
    return my
    """
def merg_JSON(json_df, ticker):
    """merges json_df and dataframe with shares volume on date. all is seperate - no loop """
    """adjusting currency"""
    filtered_port=portfolio_conn()[(portfolio_conn()['ticker']==ticker)]
    final=json_df.iloc[:,[0,4]]
    nfinal=pd.merge(final,filtered_port,on='date', how='left')
    nfinal['sum_on_date']=nfinal['sum_on_date'].ffill()  #it fills all cells beneath with the last provided value in sum_on_date column
    nfinal['currency']=nfinal['currency'].ffill() #it fills all cells beneath with the last provided value in currency column
    nfinal['currency_value']=nfinal.apply()
    nfinal['value']=nfinal['close']*nfinal['sum_on_date'] #value of all shares per asset
    #nfinal['value']=nfinal.apply(lambda x: if)
    #final=wig20.iloc[:,[0,4]]
    #nfinal.plot(x='date', y='value')
    #plt.show()
    return nfinal #.groupby('sum_on_date').sum()
df_pekabex=merg_JSON(pekabex,'pekabex')
df_wig20=merg_JSON(wig20,'wig20')
df_nasdaq100=merg_JSON(nasdaq100,'nasdaq100')
list_dataframes=[df_pekabex,df_wig20,df_nasdaq100]
def moje_portfolio():
    """it merges all positions into one Dataframe. Then it Displays NOMINAL value of portfolio"""
    my=reduce(lambda left, right: pd.merge(left,right, on='date', how='left'),list_dataframes)
    #my=pd.merge(df_pekabex,df_wig20, df_nasdaq100, on='date',how='left') #trzeba mergować kilka na raz
    my['all_stocks_value']=my.iloc[:,7::7].sum(axis=1) #it sums every 6th column startiing from 6th(value
    #my['all_stocks_value']=my['value_x']+my['value_y'] #summing value of each position/purchase/sell to 1 column over the days
    pd.set_option('display.max_columns', None)
    my
    print(my)
    my.plot(x='date',y='all_stocks_value')
    plt.show()
    return my
    #my.plot(x='date',y='value')
    #plt.show()
print(moje_portfolio())

