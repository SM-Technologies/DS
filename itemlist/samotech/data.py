import pandas as pd
import os
import sys


# #Read json from my scraper

def call_scraper(search):
    """
    This function calls my Scraper with an input search
    """
    search_str = f'"{search}"'
    scraper = os.system(f'scrapy crawl samotech -a search={search_str}')
    print(type(scraper))
    df = pd.read_json('scraper.json', encoding='utf-8')
    return df


# Data Cleaning
def df_clean(df):
    """
    Data cleaning, and str convertion
    """
    # convert to DataFrame
    df = pd.DataFrame(df)
    df['store'] = df['store'].str.get(0)
    df['name'] = df['name'].str.get(0)
    df['link'] = df['link'].str.get(0)
    df['imageURL'] = df['imageURL'].str.get(0)
    df['Price'] = df['Price'].str.get(0)
    df['description'] = df['description'].str.join(', ')
    df['description'] = df['description'].str.replace(", ,", "")
    # Drop NaN values
    df = df.dropna()
    # Sort values by store (optional)
    df.sort_values(by=['store'])
    # split price colum into twy , currency and price
    df[['currency', 'Price']] = df.Price.str.split('  ', expand=True)
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = df['Price'].str.replace('\s', '')
    # Price Convertion to numeric
    df['Price'] = pd.to_numeric(df['Price'])
    return df


def precios(df):
    """
    Price convertion
    """
    df.loc[df['currency'] == 'US', 'Price'] = df['Price']*3800
    df.loc[df['currency'] == 'US', 'currency'] = 'COP'
    df.loc[df['currency'] == 'C', 'Price'] = df['Price']*111
    df.loc[df['currency'] == 'C', 'currency'] = 'COP'
    df.loc[df['currency'] == 'GBP', 'Price'] = df['Price']*5000
    df.loc[df['currency'] == 'GBP', 'currency'] = 'COP'
    df.loc[df['currency'] == 'EUR', 'Price'] = df['Price']*4500
    df.loc[df['currency'] == 'EUR', 'currency'] = 'COP'
    return df


if __name__ == "__main__":
    # Remove previous search
    try:
        os.remove("df.json")
        print('Searching for scraped data...')
    except FileNotFoundError as nofile:
        print('No Data Frame found. \nSearching for previously scraped data...')
    try:
        os.remove("scraper.json")
        print('Previously scraped data removed. \nStarting Scraper...')
    except FileNotFoundError as nofile:
        print('No file found. \nStarting Scraper...')
    # Launch Scraper with My Search
    search = sys.argv[1]
    df = call_scraper(search)
    # cleanin my DataFrame
    df = df_clean(df)
    # DataFrame with Converted Prices
    df = precios(df)

    # Sorting By Price
    df_o = df.sort_values(by=['Price'])
    df_o = df_o[['store', 'name', 'link', 'imageURL',
                 'currency', 'Price', 'description']]
    print(df_o.head(1))
    # Export DataFrame
    df_o.to_json(r'df.json', orient='records', indent=4, force_ascii=True)
