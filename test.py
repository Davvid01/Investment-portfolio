import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  #  'Agg' or 'Qt5Agg'

def api_fetch():
    demo_url=f'https://eodhd.com/api/eod/AAPL.US?from=2024-01-01&period=d&api_token=DEMO&fmt=json'
    try:
        response=requests.get(demo_url)
        response.raise_for_status()
        data=response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None
print(api_fetch())

df=pd.DataFrame(api_fetch())
print(df)

print(df.iloc[:,2::2])
#df=df.iloc[:,2::2]
df['nowy']=df.iloc[:,2::2].sum(axis=1)
#df['nowy']=df.apply((lambda x:))
print(df)

#df.iloc[:,6::6] #start on 6th column, iterate every 6th column