#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Standard modules
#===============================================================================
#from util_inspect import get_self


#===============================================================================
#--- SETUP external modules
#===============================================================================
import scrapy
import json
from scrapy.crawler import CrawlerProcess
#===============================================================================
#--- SETUP Custom modules
#===============================================================================
#from util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================

def start_python_console(namespace=None, noipython=False, banner=''):
    """Start Python console binded to the given namespace. If IPython is
    available, an IPython console will be started instead, unless `noipython`
    is True. Also, tab completion will be used on Unix systems.
    """
    if namespace is None:
        namespace = {}

    try:
        try: # use IPython if available
            if noipython:
                raise ImportError()
            try:
                from IPython import start_ipython
                start_ipython([], user_ns=namespace)
            except Exception as e:
                import ipdb; ipdb.set_trace()

        except ImportError:
            import code
            try: # readline module is only available on unix systems
                import readline
            except ImportError:
                pass
            else:
                import rlcompleter
                readline.parse_and_bind("tab:complete")
            code.interact(banner=banner, local=namespace)
    except SystemExit: # raised when using exit() in python code.interact
        pass


# Pipeline to write results
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('quoteresult.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

def parse(keyword, place):
    logging.warning("Running on {} {}".format(keyword,place))








class Spider_DownloadPage2(scrapy.Spider):
    name = "Spider_DownloadPage"

    #def __init__(self, *args, **kwargs): 
#     def __init__(self, *args, **kwargs):        
#         super().__init__()
        #super(MySpider, self).__init__(*args, **kwargs) 
        #print("INIT")
        #print(self)
        #print(self.start_urls)
        #self.start_urls = [kwargs.get('start_urls')] 
        #raise
        #self.start_urls = my_urls   

    #location_url = r"https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
#     location_url = r"http://quotes.toscrape.com/page/1/"
#     start_urls = [
#          location_url,
#      ]
    
    #print(4response)
    def parse(self, response):
        logging.critical("Response: {}".format(response.url))
        #filename = response.url.split("/")[-1] + '.html'
        filename = "downloaded" + '.html'
        logging.info("Writing to file {}".format( filename))
        with open(filename, 'wb') as f:
            f.write(response.body)
        



def scrapy_exec_download_page(spider, location_urls):
    #location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    logging.critical("Spider: {}, {}".format(spider.name,location_urls))

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    
    logging.critical("Process: {}".format(process))
    this_spider = Spider_DownloadPage1(start_urls=location_urls)
    print(this_spider)
    print(this_spider.start_urls)
    print(type(this_spider.start_urls))
    print(type(this_spider.start_urls[0]))
    #raise
    process.crawl(this_spider)
    logging.critical("Starting {}".format(process))
    process.start()
    logging.critical("Finished {}".format(process))
    #print()

class Spider_GlassDoor(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'quoteresult.json'                        # Used for pipeline 2
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }


def glassdoor_parse1(location):
    class Spider_GlassDoorDownloadPage(scrapy.Spider):
        name = "Spider_GlassDoorDownloadPage"
        #location_url = r"http://quotes.toscrape.com/page/1/"
        location_url = r"https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    
        start_urls = [
            location_url,
        ]
    
        def parse(self, response):
            
            filename = response.url.split("/")[-1] + '.html'
            filename = "downloaded" + '.html'
            logging.info("Writing to file {}".format( filename))
            with open(filename, 'wb') as f:
                
                f.write(response.body)
                
    
    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    logging.debug("Download page: {}".format(location_url))
    # Glassdoor spider

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    
    logging.critical("Process: {}".format(process))
    process.crawl(Spider_GlassDoor(start_urls=[location_url]))
    
    logging.critical("Starting: {}".format(process))
    process.start()


def run():
    #--- Spider
    class MySpiderSpider(scrapy.Spider):
        name = "Spider_DownloadPage"
        
        def parse(self, response):
            print("*******************")
            print("*******************")
            print("*******************")
            logging.critical("Response: {}".format(response))
            filename = "downloaded" + '.html'
            logging.info("Writing to file {}".format( filename))
            raise
            with open(filename, 'wb') as f:
                f.write(response.body)
            print("*******************")
            print("*******************")
            print("*******************")
                        
    #--- Execute the spider
    process = CrawlerProcess()
    process.crawl(MySpiderSpider, start_urls=[r"http://quotes.toscrape.com/page/1/"] )
    process.start()


# def run():
#     test()
#     #raise
#     #location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
#     location_urls = [r"http://quotes.toscrape.com/page/1/"] 
    #scrapy_exec_download_page(Spider_DownloadPage1,location_urls)
    
    
#     process = CrawlerProcess({
#         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#     })
#     
#     print(process)
#     
#     location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
#     process.crawl(GlassSpider(start_urls=[location_url]))
#     process.start()    
    #raise

if __name__ == "__main__":
    #logging.getLogger('scrapy').propagate = False
    run()
