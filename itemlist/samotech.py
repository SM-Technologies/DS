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

class SamotechCrawler(CrawlSpider):
    name = 'Samotech'
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
        'COOKIES_ENABLED': True,
        # 'CLOSESPIDER_PAGECOUNT' : 3, # si no se limita el Scraper recorre todas las paginas
        #Configuración de Scrapoxy tambien se debe inicializar con scrapoxy start conf.json -d
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 16,
        'RETRY_TIMES' : 0,
        'PROXY':'http://127.0.0.1:8888/?noconnect',
        'API_SCRAPOXY' : 'http://127.0.0.1:8889/api',
        'API_SCRAPOXY_PASSWORD' : 'Zxsa1254',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapoxy.downloadmiddlewares.proxy.ProxyMiddleware': 100,
            'scrapoxy.downloadmiddlewares.wait.WaitMiddleware': 101,
            'scrapoxy.downloadmiddlewares.scale.ScaleMiddleware': None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        },
        'DEPTH_LIMIT':2
    }

    allowed_domains = ['amazon.com']

    # start_urls = ['https://www.amazon.com/s?k=camisas+blancas']
    start_urls = ['https://www.amazon.com/s?k=macbook&ref=nb_sb_noss_2']
    
    
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
        