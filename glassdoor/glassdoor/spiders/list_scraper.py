from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy.conf import settings


class List_Spider(CrawlSpider):
    name = "glassdoor_list_hunter"

    def __init__(self, country=None, city=None,):

        self.allowed_domains = ["glassdoor.com",
                                "glassdoor.de",
                                ]

        self.start_urls = [
            'https://www.glassdoor.de/Job/berlin-data-science-jobs-SRCH_IL.0,6_IC2622109_KO7,19.htm',
            'https://www.glassdoor.de/Job/k%C3%B6ln-data-science-jobs-SRCH_IL.0,4_IC4348509_KO5,17.htm'

        ]

        self.page_count = 0
        self.room_count = 0

    def parse(self, response):
        if response.status > 299:
            pass
        else:
            jobs_titles = response.xpath(
                '//div[@class="flexbox"]/div/a/text()').extract()
            companies = [repr(company.strip()).split(' \\')[0] for company in
                         response.xpath('//div[@class="flexbox empLoc"]/div/text()'
                                        ).extract() if '\\' in repr(company)]
            cities = response.xpath(
                '//span[@class="subtle loc"]/text()').extract()
            # here job_links= ....
            # for link in job_lings:
            #    job_page = "glassdoor.de" + link
            #    yield Request(job_page, meta={
            #        'dont_redirect': True,
            #    }, callback=self.parse_job,)



            # for f, b, a in zip(jobs_titles, companies, cities):
            #     print(f, b, a)

            if '_IP' in response.url:
                pass
            else:
                next_page = response.url.split('.htm')[0] + '_IP2' + '.htm'
                yield Request(next_page, meta={
                    'dont_redirect': True,
                }, callback=self.parse,)

    def parse_job(job, response):
        response.xpath('//div[@class="jobDescriptionContent desc"]').extract()
        response.xpath(
            '//div[@class="jobDescriptionContent desc"]/text()').extract()
