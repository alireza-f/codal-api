from scrapy.crawler import CrawlerRunner

from Gradientdp.codal.spiders.gradient import GradientSpider

url = 'https://codal.ir/ReportList.aspx?search&Symbol=%D8%B4%D9%BE%D9%86%D8%A7&LetterType=20&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&Consolidatable&NotConsolidatable'
process = CrawlerRunner()
process.crawl(GradientSpider, symbol_url = url)
# process.start()