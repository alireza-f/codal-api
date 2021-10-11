import crochet
crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time

from scrapy.utils.project import get_project_settings
import os
from Gradientdp.codal.spiders.gradient import GradientSpider


app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner(get_project_settings())


@app.route('/')
def index():
	return render_template("index.html") 


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['symbol'] 
        global baseURL
        baseURL = f'https://codal.ir/ReportList.aspx?search&Symbol={s}&LetterType=20&AuditorRef=-1&PageNumber=1&Audited&NotAudited&IsNotAudited=false&Childs&Mains&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&Consolidatable&NotConsolidatable'
        if os.path.exists("Gradientdp/output.json"): 
        	os.remove("Gradientdp/output.json")
        return redirect(url_for('scrape'))


@app.route("/scrape")
def scrape():
    scrape_with_crochet(baseURL=baseURL)
    time.sleep(20) 
    return jsonify(output_data) 
  

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(GradientSpider, symbol_url = baseURL)
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__== "__main__":
    app.run(debug=True)