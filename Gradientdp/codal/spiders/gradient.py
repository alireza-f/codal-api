
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup as bs

from unidecode import unidecode

class MyItem(scrapy.Item):
    name = scrapy.Field()
    dps = scrapy.Field()
    date = scrapy.Field()


class GradientSpider(scrapy.Spider):
    name = 'gradient'
    # start_urls = ['https://codal.ir/ReportList.aspx?search&Symbol=%D9%88%D8%AC%D8%A7%D9%85%DB%8C&LetterType=20&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&Consolidatable&NotConsolidatable',]
    myBaseUrl = ''
    start_urls = []
    def __init__(self, symbol_url='', **kwargs): 
        super().__init__(**kwargs)
        self.myBaseUrl = symbol_url
        self.start_urls.append(self.myBaseUrl)

    custom_settings = {'FEED_URI': 'Gradientdp/output.json', 'CLOSESPIDER_TIMEOUT' : 50} 

    def start_requests(self):
            for url in self.start_urls:
                yield SplashRequest(url, self.parse, args={'wait': 5})


    def parse(self, response):
        tbody = response.css('tbody.scrollContent')
        row = tbody.css('tr.table__row.ng-scope')
        col = row.css('td')
        links = col.css('a.letter-title.ng-binding.ng-scope::attr(href)')
        for link in links:
            # print('**********THERE IS NO BUG**********')
            yield response.follow("https://www.codal.ir"+link.get(), callback=self.parse_page)


    def parse_page(self, response):

        page = bs(response.text, 'html.parser')
        name = page.find('head', id='Head1').text.strip().split('(')[-1]
        name = name.replace(')', '').strip()
        try:
            tables = page.find_all('tr', class_="ComputationalRow")
            for tr in tables:
                if "سود نقدی هر سهم" in tr.text:
                    dps = int(unidecode(tr.find('span', class_='spanFormattedValue').text).replace(',', ''))
            table_head = page.find('table', {'id':'ucAssemblyPRetainedEarning_grdAssemblyProportionedRetainedEarning'})
            date = table_head.findAll('th')[-1].text.split(' ')[3]
            yield MyItem(name=name, dps=dps, date=date)
        except:
            pass

            
