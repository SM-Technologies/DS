import pandas as pd
import os
import sys

# #Read json from my scraper
search=sys.argv[1]
scraper = os.system(f'scrapy crawl samotech -a search="{search}"')
df = pd.read_json('scraper.json',encoding='utf-8')

#convert to DataFrame
df = pd.DataFrame(df)

# Data Cleaning 
df['tienda'] = df['tienda'].str.get(0)
df['nombre'] = df['nombre'].str.get(0)
df['url'] = df['url'].str.get(0)
df['img'] = df['img'].str.get(0)
df['precio'] = df['precio'].str.get(0)
df['descripcion'] = df['descripcion'].str.join(', ')
df['descripcion'] = df['descripcion'].str.replace(", ,","")

df=df.dropna()

df.sort_values(by=['tienda'])

df[['moneda','precio']]=df.precio.str.split('  ',expand=True)
df['precio'] = df['precio'].str.replace(',','')
df['precio'] = df['precio'].str.replace('\s','')

# Price Convertion
df['precio']=pd.to_numeric(df['precio'])

def precios(df):
    df.loc[df['moneda'] == 'US', 'precio'] = df['precio']*3800
    df.loc[df['moneda'] == 'US', 'moneda'] = 'COP'
    df.loc[df['moneda'] == 'C', 'precio'] = df['precio']*111
    df.loc[df['moneda'] == 'C', 'moneda'] = 'COP'
    df.loc[df['moneda'] == 'GBP', 'precio'] = df['precio']*5000
    df.loc[df['moneda'] == 'GBP', 'moneda'] = 'COP'
    return df

# DataFrame with Converted Prices
df= precios(df)

# Sorting By Price
df_o=df.sort_values(by=['precio'])
df_o=df_o[['tienda','nombre','url','img','moneda','precio','descripcion']]

print(df_o.head(1))
#Export DataFrame
df_o.to_json(r'df.json', orient='records',indent=4,force_ascii=True)


