from pathlib import Path

import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobsmanorama"

    def __init__(self):
        self.page_next = 0

    def start_requests(self):
        urls = [
            "https://www.onmanorama.com/content/mm/en/topic/general-topics/masterarticle/_jcr_content/mastercontent"
            "/topiclisting.moretopicresults.0.50.Onmanorama:topic~general-topics~21~job.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = "https://www.onmanorama.com"
        if (response.css("h2.listing-title-002").get() != None):
            for job in response.css("h2.listing-title-002"):
                parsed_url = job.css("h2.listing-title-002 a::attr(href)").get()
                if parsed_url:
                    data_url = base_url + parsed_url
                    title = job.css("h2.listing-title-002 a::text").get()
                    yield {
                        "mainUrl": response.url,
                        "url": data_url,
                        "title": title
                    }
                else:
                    break
            self.page_next = self.page_next + 51
            next_page_url = "https://www.onmanorama.com/content/mm/en/topic/general-topics/masterarticle/_jcr_content/mastercontent/topiclisting.moretopicresults." + str(
                self.page_next) + ".50.Onmanorama:topic~general-topics~21~job.html"
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            return
