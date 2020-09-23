from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    url = Field()
    img = Field()

class AmazonCrawler(CrawlSpider):
    name = 'Amazon'
    custom_settings={
        'FEEDS':{
            'listado.json':{
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            }
        },
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'ROBOTSTXT_OBEY' : True,
        'DOWNLOAD_DELAY' : 0.3,
        'COOKIES_ENABLED': True,
#         'DOWNLOADER_MIDDLEWARES': {
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
# },
        'DEPTH_LIMIT': 10
    }
        # 'PROXY_POOL_ENABLED': True
        # 'DOWNLOADER_MIDDLEWARES' : {'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 500}
        # 'CUSTOM_PROXY' : 'https://168.169.96.2:800'
        # 'CLOSESPIDER_PAGECOUNT' : 20,
    
    allowed_domains = ['amazon.com']

    start_urls = ['https://www.amazon.com/s?k=headset']
    # CUSTOM_PROXY = "https://168.169.96.2:800"
    
    
    rules =(
        #Paginacion
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/ul[@class="a-pagination"]/li/a')
            ),follow= True

        ),
        # Detalle Productos
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/h2/a[@class="a-link-normal a-text-normal"]')
            ),follow= True, callback= 'parse_items'
        ),
    
    )

    def textCleaning(self,text):
        """
        Funcion para limpiar el texto obtenido
        """
        newText = text.replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
        return newText

    def parse_items(self,response):
        """
        Funcion que se encarga de extraer la información de cada producto.
        """
        try:
            link = response.url
            image = response.xpath('//div[@class="imgTagWrapper"]/img/@data-old-hires').extract()
            item = ItemLoader(Articulo(),response)

            item.add_value('url',link)
            item.add_value('img',image)
            item.add_xpath('nombre','//h1[@id="title"]/span/text()', MapCompose(self.textCleaning))
            item.add_xpath('precio','//span[@id="priceblock_ourprice"]/text()')
            item.add_xpath('descripcion','//div[@id="feature-bullets"]/ul/li/span/text()',MapCompose(self.textCleaning))
            
            yield item.load_item()
        except:
            print(response.url)
        