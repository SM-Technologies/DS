# DataScience

[![Scrapy](https://miro.medium.com/max/700/1*7KVe2szj1rjt1_Jlmdznkw.png)](https://scrapy.org)

This is the repo for out Web Scraper in Samotech project. Its based in Scrapy and use Pandas to clean the data.

Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. Pandas is an open source Python library that allows users to explore, manipulate and visualise data in an extremely efficient manner. It is literally Microsoft Excel in Python.

You can find our documentation here:
[![Notion](https://larocqueinc.com/wp-content/uploads/2020/04/Notion-Logo.png)](https://www.notion.so/Development-737e4ccbc7d9409d98ab6d2aaacaa517)

Once Scrapy project is configured as documentation says, our starting point would be data.py located in the root of Samotech project.
This python script is responsible for start our scraper with a search input. 
```sh
$ python data.py "<item to find>"
```
This command line starts our scraper so it will be crawling Amazon, Mercado Libre and Ebay for the product of interestt After a few seconds we got a json with all our data and is time for pandas to come to action. With pandas toolbox we are able to clean the data, convert prices, sort this prices and format the dataframe to an easy to read new json with all the information we need.

This is the DF as it comes from the scraper:

![DF_Scraper](https://user-images.githubusercontent.com/51537670/96348583-86910f80-106f-11eb-9d57-9a6c85df50db.png)
there are some characters and formats that are not useful for our purpose, so first step is getting rid of those brackets and NaN values and this is the result.
![Cleaning](https://user-images.githubusercontent.com/51537670/96348606-a88a9200-106f-11eb-8efd-af0da96c067c.png)
Now in Price Column we got different currency, so aour approach was to separate this in two columns and convert prices to COP.
![PriceConv](https://user-images.githubusercontent.com/51537670/96348622-cce66e80-106f-11eb-9935-9ea217109f4e.png)
With this a new json its generated wich contains clean and ordered data.
![FinalDF](https://user-images.githubusercontent.com/51537670/96348635-e2f42f00-106f-11eb-9d1c-a3bef84a42f9.png)
