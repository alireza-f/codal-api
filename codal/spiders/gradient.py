
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
    start_urls = ['https://codal.ir/ReportList.aspx?search&Symbol=%D8%B4%D9%BE%D9%86%D8%A7&LetterType=20&Isic=232007&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=0&Category=-1&CompanyType=1&Consolidatable&NotConsolidatable',]

    def start_requests(self):
            for url in self.start_urls:
                yield SplashRequest(url, self.parse, args={'wait': 5})


    def parse(self, response):
        
        tbody = response.css('tbody.scrollContent')
        row = tbody.css('tr.table__row.ng-scope')
        col = row.css('td')
        links = col.css('a.letter-title.ng-binding.ng-scope::attr(href)')
        for link in links:
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

            
