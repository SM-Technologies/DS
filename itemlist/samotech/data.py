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
df['store'] = df['store'].str.get(0)
df['name'] = df['name'].str.get(0)
df['link'] = df['link'].str.get(0)
df['imageURL'] = df['imageURL'].str.get(0)
df['Price'] = df['Price'].str.get(0)
df['description'] = df['description'].str.join(', ')
df['description'] = df['description'].str.replace(", ,","")

df=df.dropna()

df.sort_values(by=['store'])

df[['curency','Price']]=df.Price.str.split('  ',expand=True)
df['Price'] = df['Price'].str.replace(',','')
df['Price'] = df['Price'].str.replace('\s','')

# Price Convertion
df['Price']=pd.to_numeric(df['Price'])

def precios(df):
    df.loc[df['curency'] == 'US', 'Price'] = df['Price']*3800
    df.loc[df['curency'] == 'US', 'curency'] = 'COP'
    df.loc[df['curency'] == 'C', 'Price'] = df['Price']*111
    df.loc[df['curency'] == 'C', 'curency'] = 'COP'
    df.loc[df['curency'] == 'GBP', 'Price'] = df['Price']*5000
    df.loc[df['curency'] == 'GBP', 'curency'] = 'COP'
    return df

# DataFrame with Converted Prices
df= precios(df)

# Sorting By Price
df_o=df.sort_values(by=['Price'])
df_o=df_o[['store','name','link','imageURL','curency','Price','description']]
df_o = df_o[1,:]
# print(df_o.head(1))
#Export DataFrame
df_o.to_json(r'df.json', orient='records',indent=4,force_ascii=True)


