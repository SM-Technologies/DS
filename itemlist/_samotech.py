from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

class Articulo(Item):
    tienda = Field()
    nombre = Field()
    precio = Field()
    descripcion = Field()
    url = Field()
    img = Field()

class SamotechCrawler(CrawlSpider):
    name = 'samotech'
    item_countA = 0
    item_countM = 0
    item_countE = 0
    custom_settings={
        'FEEDS':{
            'listado.json':{
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            },
        },
        'FEED_EXPORT_FIELDS':['tienda','nombre','url','img','precio','descripcion'],
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        # 'ROBOTSTXT_OBEY' : True,
        'COOKIES_ENABLED': False,
        #Configuración de Scrapoxy tambien se debe inicializar con scrapoxy start conf.json -d
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 16,
        'CLOSESPIDER_ITEMCOUNT':48,
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
    }

    def __init__(self,search='',*args,**kwargs):
        super(SamotechCrawler, self).__init__(*args, **kwargs)
        self.start_urls = [
        'https://www.amazon.com/s?k='+search.replace(' ','+'),
        'https://listado.mercadolibre.com.co/'+search.replace(' ','-'),
        'https://www.ebay.com/sch/i.html?_from=R40&_nkw='+search.replace(' ','+')
        ]
        self.allowed_domains = ['amazon.com',
                       'articulo.mercadolibre.com.co',
                       'listado.mercadolibre.com.co',
                       'ebay.com'
                                ]
        
    rules =(
        #Paginacion
        #Amazon
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/ul[@class="a-pagination"]/li/a')
            ),follow= True
        ),
        
        #MercadoLibre
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/ul/li[contains(@class,"button--next")]/a')
        ),follow = True
        ),
        #Ebay
        Rule(
            LinkExtractor(
                restrict_xpaths=('//a[@class="pagination__next"]')
            ),follow = True
        ),

        # Detalle Productos
        #Amazon
        Rule(
            LinkExtractor(
                restrict_xpaths=('//div/h2/a[@class="a-link-normal a-text-normal"]')
            ),follow= True, callback= 'parse_items'
        ),
        #MercadoLibre
        Rule(
            LinkExtractor(
                allow=r'/MCO-'
            ),follow= True, callback= 'parse_itemsML'
        ),
        #Ebay
        Rule(
            LinkExtractor(
                allow=r'/itm/'
            ),follow= True, callback= 'parse_itemsEb'
        ),
    
    )

        

    def textCleaning(self,text):
        """
        Funcion para limpiar el texto obtenido
        """
        newText = text.replace('\n',' ').replace('\r',' ').replace('\t',' ').replace('<p>',' ').replace('<br>',' ').replace('</p>',' ').replace('</br>',' ').strip()
        return newText

    def priceCleaning(self,text):
        """
        Funcion para limpiar el precio obtenido
        """
        newText = text.replace('$',' ').strip()
        return newText

    def parse_items(self,response):
        """
        Funcion que se encarga de extraer la información de cada producto.
        """
        item = ItemLoader(Articulo(),response)

        if self.item_countA < 16:
            link=response.url
            image= response.xpath('//div[@class="imgTagWrapper"]/img/@data-old-hires').extract()
                    
            item.add_value('tienda','Amazon')
            item.add_value('url',link),
            item.add_value('img',image),
            item.add_xpath('nombre','//h1[@id="title"]/span/text()', MapCompose(self.textCleaning)),
            item.add_xpath('precio','//span[@id="priceblock_ourprice"]/text()', MapCompose(self.priceCleaning)),
            item.add_xpath('descripcion','//div[@id="feature-bullets"]/ul/li/span/text()',MapCompose(self.textCleaning))
            yield item.load_item()    
            self.item_countA= self.item_countA+1        
        else:
            print('Limit reached for Mercado Libre') 
        
        if self.item_countA + self.item_countE + self.item_countM == 48:
            raise CloseSpider('item limit reached')
        
    

    def parse_itemsML(self,response):
        """
        Funcion que se encarga de extraer la información de cada producto en Mercadolibre.
        """
        item = ItemLoader(Articulo(),response)

        if self.item_countM < 16:
            link = response.url
            item.add_value('tienda','MercadoLibre')
            item.add_value('url',link)
            item.add_xpath('img','//figure[contains(@class,"thumbgallery_default-0")]/a/@href')
            item.add_xpath('nombre','//header[@class="item-title"]/h1/text()', MapCompose(self.textCleaning))
            item.add_xpath('precio','//span[@class="price-tag-fraction"]/text()', MapCompose(self.priceCleaning))
            item.add_xpath('descripcion','//section[contains(@class,"item-description")]/div/div[@class="item-description__text"]/p',MapCompose(self.textCleaning))
            yield item.load_item()
            self.item_countM= self.item_countM+1
        else:
            print('Limit reached for Mercado Libre')
            
        
        if self.item_countA + self.item_countE + self.item_countM == 48:
            raise CloseSpider('item limit reached')

    def parse_itemsEb(self,response):
        """
        Funcion que se encarga de extraer la información de cada producto en Mercadolibre.
        """
        item = ItemLoader(Articulo(),response)

        if self.item_countE < 16:
            link = response.url
            item.add_value('tienda','Ebay')
            item.add_value('url',link)
            item.add_xpath('img','//figure[contains(@class,"thumbgallery_default-0")]/a/@href')
            item.add_xpath('nombre','//h1[@id="itemTitle"]/text()[1]')
            item.add_xpath('precio','//span[@id="prcIsum"]/text()', MapCompose(self.priceCleaning))
            item.add_xpath('descripcion','//div[@id="ds_div"]//text()') 
            yield item.load_item()
            self.item_countE= self.item_countE+1 
        else:
            print ('Limit reached for Ebay')
        if self.item_countA + self.item_countE + self.item_countM == 48:
            raise CloseSpider('item limit reached')
        
