import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Możesz też spróbować 'Agg' lub 'Qt5Agg'
#url=f''
#data=requests.get(url).json()

#with open('API Pekabex.txt', 'etfbw20TR.WAR' 'r', encoding='utf-8') as f:
#    content=f.read()
def opening(file):
    with open(f'{file}', 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            data = json.loads(content)
            print(data)
            return data
        except json.JSONDecodeError as e:
            print("Bład parsowania JSON: ", e)
        print(type(data))
pekabex=opening('API Pekabex.txt')
wig20=opening('etfbw20TR.WAR.txt')

print(pekabex)
print(type(pekabex))

def to_df(df):
    ndf=pd.DataFrame(df)
    ndf = ndf.drop('warning', axis=1, errors='ignore')  # required to specify row=-0 or column=1
    return ndf
pekabex=to_df(pekabex)
wig20=to_df(wig20)
"""
pekabex.plot(x='date', y='close')
wig20.plot(x='date', y='close')
plt.show()
"""
def dicts():
    """Zwraca DataFrame z historią transakcji (kupna/sprzedaży)."""
    pkbd = [{'date': '2024-02-26', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex'},
            {'date': '2024-02-29', 'volume': 5, 'operation': 'buy', 'ticker': 'pekabex'},
            {'date': '2024-03-01', 'volume': 4, 'operation': 'sell', 'ticker': 'pekabex'}]
    wig20d = [{'date': '2024-02-26', 'volume': 11.3675, 'operation': 'buy', 'ticker': 'wig20'},
              {'date': '2025-01-23', 'volume': 0, 'operation': 'buy', 'ticker': 'wig20'}]
    df_combined = pd.DataFrame(pkbd + wig20d)
    return df_combined
transakcje=dicts()
print(transakcje)
def portfolio_conn():
    """Tworzy portfel inwestycyjny, sumuje liczbę akcji i oblicza wartość portfela."""
    connector=transakcje
    #connector['sum_on_date']=""
    connector['volume']=connector.apply(lambda row: row['volume'] if row['operation']=='buy' else -row['volume'], axis=1) # trying to compare an entire Series (connector['operation']) to a single value ('buy') within the lambda function. To fix this, we need to modify the lambda function to operate on individual rows. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
    connector['sum_on_date']=connector['volume'].cumsum() #it sums rows conecutively
    connector['sum_on_date'] = connector.groupby('ticker')['volume'].cumsum()
    #connector['sum_on_date']=connector['volume'] #[for x in connector['ticker']:] #.expanding().sum() #connector['volume'].map(lambda x:x+x[0])

    #for index, row in connector.itterows():
     #   if x==d0:
     #       connector['sum_on_date']=connector['sum_on_date']+connector['volume']

      #  d0=x
    return connector
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
print(portfolio_conn())

def merg_JSON(json_df, ticker):
    filtered_port=portfolio_conn()[(portfolio_conn()['ticker']==ticker)]
    print(f'gdzie ten tekst: {str(json)}')
    final=json_df.iloc[:,[0,4]]
    nfinal=pd.merge(final,filtered_port,on='date', how='left')
    nfinal['sum_on_date']=nfinal['sum_on_date'].ffill()
    nfinal['value']=nfinal['close']*nfinal['sum_on_date']
    #final=wig20.iloc[:,[0,4]]
    #nfinal.plot(x='date', y='value')
    #plt.show()
    return nfinal #.groupby('sum_on_date').sum()
df_pekabex=merg_JSON(pekabex,'pekabex')
df_wig20=merg_JSON(wig20,'wig20')

def moje_portfolio():
    my=pd.merge(df_pekabex,df_wig20, on='date',how='left')
    my['all_stocks_value']=my['value_x']+my['value_y']
    pd.set_option('display.max_columns', None)
    my
    my.plot(x='date',y='all_stocks_value')
    plt.show()
    return my
    #my.plot(x='date',y='value')
    #plt.show()
print(moje_portfolio())

