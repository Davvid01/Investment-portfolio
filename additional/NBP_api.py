import requests
import json
import pandas as pd

def api_fetch(link):
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
    df_currency= pd.DataFrame(json['rates'])
    df_currency=df_currency.rename(columns={"effectiveDate":"date"}).drop(columns='no')
    return df_currency
print(to_df(usd))