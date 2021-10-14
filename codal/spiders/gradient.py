
import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup as bs

from unidecode import unidecode

from ..items import CodalItem


class GradientSpider(scrapy.Spider):
    name = 'gradient'

    start_urls = ['https://codal.ir/ReportList.aspx?search&Symbol=%D8%AE%D9%88%D8%AF%D8%B1%D9%88&LetterType=20&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&Consolidatable&NotConsolidatable',
                  'https://codal.ir/ReportList.aspx?search&Symbol=%D8%AE%D8%B3%D8%A7%D9%BE%D8%A7&LetterType=20&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&Consolidatable&NotConsolidatable',

                  ]

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
        items = CodalItem()
        page = bs(response.text, 'html.parser')
        name = page.find('head', id='Head1').text.strip().split('(')[-1]
        name = name.replace(')', '').strip()
        try:
            tables = page.find_all('tr', class_="ComputationalRow")
            for tr in tables:
                if "سود نقدی هر سهم" in tr.text:
                    dps = int(
                        unidecode(tr.find('span', class_='spanFormattedValue').text).replace(',', ''))
            table_head = page.find('table', {
                                   'id': 'ucAssemblyPRetainedEarning_grdAssemblyProportionedRetainedEarning'})
            date = table_head.findAll('th')[-1].text.split(' ')[3]

            items['name'] = name
            items['dps'] = dps
            items['date'] = date
            yield items
        except:
            pass
