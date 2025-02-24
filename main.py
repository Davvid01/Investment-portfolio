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
    ndf = ndf.drop('warning', axis=1)  # required to specify row=-0 or column=1
    return ndf
pekabex=to_df(pekabex)
wig20=to_df(wig20)

pekabex.plot(x='date', y='close')
wig20.plot(x='date', y='close')
plt.show()


