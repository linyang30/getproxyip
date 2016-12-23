# -*- coding: utf-8 -*-
import scrapy
from getproxyip.items import GetproxyipItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://www.xicidaili.com/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }

    def start_requests(self):
        reqs = []
        for i in range(5):
            req = scrapy.Request('http://www.xicidaili.com/nn/%d' % i, headers=self.headers)
            reqs.append(req)
        return reqs

    def parse(self, response):
        trs = response.xpath('//table[@id = "ip_list"]')[0].xpath('tr')
        items = []
        for ip in trs[1:]:
            pre_item = GetproxyipItem()
            pre_item['IP'] = ip.xpath('//td[2]/text()')[0].extract()
            pre_item['PORT'] = ip.xpath('//td[3]/text()')[0].extract()
            pre_item['POSITION'] = ip.xpath('//td[4]/a/text()')[0].extract()
            pre_item['TYPE'] = ip.xpath('//td[6]/text()')[0].extract()
            pre_item['SPEED'] = ip.xpath('//td[7]/div[@class="bar"]/@title')[0].extract()[:-1]
            pre_item['LAST_CHECK_TIME'] = ip.xpath('//td[10]/text()')[0].extract()

            items.append(pre_item)
        return items

