import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from functools import reduce
import numpy
import requests
matplotlib.use('TkAgg')  #  'Agg' or 'Qt5Agg'

def api_fetch(link):
    """pobranie API"""
    try:
        url=link #gotta be left merge, stocks api has only 250 days back. so to match correctly stock df will be left DF.
        response=requests.get(link)
        response.raise_for_status()
        api_json=response.json()
        return api_json
    except requests.exceptions.RequestException as e:
        print(f'Error handling: {e}')
        return None
usd=api_fetch(f'https://api.nbp.pl/api/exchangerates/rates/a/usd/last/255/?format=json')
gbp=api_fetch(f'https://api.nbp.pl/api/exchangerates/rates/a/gbp/last/255/?format=json')

print(usd)

def to_df(json):
    """to DF NBP"""
    df_currency= pd.DataFrame(json['rates'])
    df_currency=df_currency.rename(columns={"effectiveDate":"date"}).drop(columns='no')
    return df_currency
usd_df=to_df(usd)
gbp_df=to_df(gbp)

"""
def api_fetch(demo_url):
        try:
            response=requests.get(demo_url)
            response.raise_for_status()
            data=response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {e}')
            return None

pekabex=api_fetch(f'https://eodhd.com/api/eod/AAPL.US?from=2024-01-01&period=d&api_token=DEMO&fmt=json')
wig20=api_fetch(f'https://eodhd.com/api/eod/AAPL.US?from=2024-01-01&period=d&api_token=DEMO&fmt=json')
nasdaq100=api_fetch(f'https://eodhd.com/api/eod/AAPL.US?from=2024-01-01&period=d&api_token=DEMO&fmt=json')
"""
pekabex=api_fetch(f'https://eodhd.com/api/eod/PBX.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
wig20=api_fetch(f'https://eodhd.com/api/eod/ETFBW20TR.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
wig40=api_fetch(f'https://eodhd.com/api/eod/ETFBM40TR.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
nasdaq100=api_fetch(f'https://eodhd.com/api/eod/CNDX.lse?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
china=api_fetch(f'https://eodhd.com/api/eod/CNYA.SW?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
semiconductor=api_fetch(f'https://eodhd.com/api/eod/SMH.LSE?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
aibigadata=api_fetch(f'https://eodhd.com/api/eod/XAIX.XETRA?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
digitalization=api_fetch(f'https://eodhd.com/api/eod/DGTL.LSE?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
uranium=api_fetch(f'https://eodhd.com/api/eod/U3O8.XETRA?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
xtb=api_fetch(f'https://eodhd.com/api/eod/XTB.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
cd_projekt=api_fetch(f'https://eodhd.com/api/eod/CDR.WAR?from=2024-01-01&period=d&api_token= 67baee1cc05d29.18192653&fmt=json')
"""
def opening(file):
    #fetching from notebook as json type for tests
    with open(f'{file}', 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            data = json.loads(content)
            print(data)
            return data
        except json.JSONDecodeError as e:
            print("Bład parsowania JSON: ", e)
        print(type(data))
"""
def to_df(df):
    ndf=pd.DataFrame(df)
    ndf = ndf.drop('warning', axis=1, errors='ignore')  # required to specify row=-0 or column=1
    return ndf

pekabex=to_df(pekabex)
wig20=to_df(wig20)
nasdaq100=to_df(nasdaq100)
wig40=to_df(wig40)
china=to_df(china)
semiconductor=to_df(semiconductor)
aibigadata=to_df(aibigadata)
digitalization=to_df(digitalization)
uranium=to_df(uranium)
xtb=to_df(xtb)
cd_projekt=to_df(cd_projekt)

def portfolio_quartelly(): #all records by/sell for quarter portfolio
    """Zwraca DataFrame z historią transakcji (kupna/sprzedaży)."""
    pkbd = [{'date': '2024-04-03', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex', 'currency':'PLN'},
            {'date': '2024-04-29', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex', 'currency':'PLN'},
            {'date': '2024-05-23', 'volume': 7, 'operation': 'buy', 'ticker': 'pekabex', 'currency':'PLN'}]
    wig20d = [{'date': '2024-12-09', 'volume': 11.3675, 'operation': 'buy', 'ticker': 'wig20', 'currency':'PLN'}]
    nasdaq100=[{'date': '2024-12-09', 'volume': 0.0898, 'operation': 'buy', 'ticker': 'nasdaq100', 'currency':'USD'}]
    china=[{'date': '2024-12-09', 'volume': 15.809, 'operation': 'buy', 'ticker': 'msci china', 'currency':'USD'}]
    mwig40=[{'date': '2024-04-22', 'volume': 1, 'operation': 'buy', 'ticker': 'mwig40', 'currency':'PLN'},
            {'date': '2024-04-25', 'volume': 1, 'operation': 'buy', 'ticker': 'mwig40', 'currency':'PLN'}]
    artificial_intelligence=[{'date': '2025-01-23', 'volume': 0.337, 'operation': 'buy', 'ticker': 'AI', 'currency':'USD'}]
    semiconductor=[{'date': '2024-12-09', 'volume': 1, 'operation': 'buy', 'ticker': 'semiconductors', 'currency':'USD'}]
    digitalisation=[{'date': '2024-04-08', 'volume': 1, 'operation': 'buy', 'ticker': 'digitalisation', 'currency':'USD'},
                    {'date': '2024-04-09', 'volume': 1, 'operation': 'buy', 'ticker': 'digitalisation', 'currency':'USD'}]
    uranium_miners=[{'date': '2024-12-09', 'volume': 2.8277, 'operation': 'buy', 'ticker': 'uranium miners', 'currency':'USD'}]
    xtb=[{'date': '2025-02-21', 'volume': 11, 'operation': 'buy', 'ticker': 'xtb', 'currency':'PLN'}]
    cd_projekt=[{'date': '2024-04-25', 'volume': 10, 'operation': 'buy', 'ticker': 'cd_projekt', 'currency':'PLN'}]
    df_combined = pd.DataFrame(pkbd+wig20d+nasdaq100+china+mwig40+artificial_intelligence+semiconductor+digitalisation+uranium_miners+xtb+cd_projekt)
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

def calculate_exchange_rate(row):
    if row['currency'] =='PLN':
        return 1
    elif row['currency'] =='USD':
        return row['mid']
    elif row['currency']=='GBP':
        return row['mid_gbp']
    else:
        return numpy.nan
def merg_JSON(json_df, ticker):
    """merges json_df and dataframe with shares volume on date. all is seperated - no loop """
    """it creates blocks, each block is particular, individual type of share, next step is to merge all apart block to one DF and summing stocks value"""
    """adjusting currency"""
    filtered_port=portfolio_conn()[(portfolio_conn()['ticker']==ticker)]
    final=json_df.iloc[:,[0,4]]
    nfinal=pd.merge(final,filtered_port,on='date', how='left')
    nfinal[f'sum_on_date']=nfinal['sum_on_date'].ffill()  #it fills all cells beneath with the last provided value in sum_on_date column
    nfinal['currency']=nfinal['currency'].ffill() #it fills all cells beneath with the last provided value in currency column
    nfinal = pd.merge(nfinal, usd_df, on='date', how='left', suffixes=('', '_usd'))
    nfinal = pd.merge(nfinal, gbp_df, on='date', how='left', suffixes=('', '_gbp'))
    nfinal['exchange_rate']=nfinal.apply(calculate_exchange_rate, axis=1)
    nfinal=nfinal.drop(columns=['mid','mid_gbp'])
    #nfinal['exchange_rate']=nfinal['currency'].apply(lambda x: usd_df['mid'] if x=='USD' else 1)
    #nfinal['currency_value']=nfinal['currency'].apply(lambda x: pd.merge(nfinal, usd_df, on='date', how='left') if x=='USD' elif x=='GBP' pd.merge(nfinal,gbp_df, on='date',how='left')  else x=1)
    nfinal['value']=nfinal['close']*nfinal['sum_on_date']*nfinal['exchange_rate'] #value of all shares per asset
    pd.set_option('display.width', 1000)
    nfinal = nfinal.set_index('date')  # Set 'date' as the index to protect it
    nfinal = nfinal.add_suffix(f'_{ticker}')  # Add suffix to all other columns
    nfinal = nfinal.reset_index()  # Restore 'date' as a column
    nfinal
    return nfinal #.groupby('sum_on_date').sum()

df_pekabex=merg_JSON(pekabex,'pekabex')
df_wig20=merg_JSON(wig20,'wig20')
df_nasdaq100=merg_JSON(nasdaq100,'nasdaq100')
df_wig40=merg_JSON(wig40,'mwig40')
df_aibigdata=merg_JSON(aibigadata,'AI')
df_msci_china=merg_JSON(china,'msci china')
df_digi=merg_JSON(digitalization,'digitalisation')
df_semiconductors=merg_JSON(semiconductor, 'semiconductors')
df_uranium=merg_JSON(uranium,'uranium miners')
df_xtb=merg_JSON(xtb,'xtb')
df_cdprojekt=merg_JSON(cd_projekt,'cd_projekt')

print(f'to jest merg_json_nasdaq: {df_nasdaq100}')
list_dataframes=[df_pekabex,df_wig20,df_nasdaq100, df_wig40, df_aibigdata, df_msci_china, df_digi, df_semiconductors,df_uranium,  df_xtb, df_cdprojekt ]

def moje_portfolio():
    """it merges all positions into one Dataframe. Then it Displays NOMINAL value of portfolio"""
    my=reduce(lambda left, right: pd.merge(left,right, on='date', how='left'),list_dataframes) #merge ensures that all rows from the "left" DataFrame are included in the result.
    #my=pd.merge(df_pekabex,df_wig20, df_nasdaq100, on='date',how='left') #trzeba mergować kilka na raz
    my['all_stocks_value']=my.iloc[:,8::8].sum(axis=1) #it sums every 8th column startiing from 9th(value
    #my['all_stocks_value']=my['value_x']+my['value_y'] #summing value of each position/purchase/sell to 1 column over the days
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    my
    print(my)
    my.plot(x='date',y='all_stocks_value')
    plt.show()
    my.to_excel('C:\Dawid\Szkola\studia\ostatni_rozdzial\Github\Stock chart\ all_values.xlsx', sheet_name='Dane do wykresu')
    return my

print(moje_portfolio())

