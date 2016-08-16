# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy import Request
from datetime import datetime, date, timedelta
from weightxreps.items import WeightxrepsItem


class UserDataByPeriod(CrawlSpider):
    name = 'weightxreps'
    allowed_domains = ['weightxreps.net']

    def __init__(self, user='danharp', start='', end='', *args, **kwargs):
        super(UserDataByPeriod, self).__init__(*args, **kwargs)
        self.user_name = user
        self.date_start = start
        self.date_end = end
        self.start_urls = ("http://weightxreps.net/journal/%s/" % user,)
        self.items = []
        self.date = None

    def recursive_parse(self, response):
        weight = response.xpath('//span[@class="weight bwnum weightunit-1"]/text()').extract()
        jbody = response.xpath('//div[@id="jbody"]')
        if weight:
            items = []
            for userText, eblock in zip(jbody.xpath('div[@class="userText"]'),
                                        jbody.xpath('div[@class="eblock"]')):
                item = WeightxrepsItem()
                item['user_name'] = self.user_name
                item['exercise_date'] = response.url[-10:]
                item['user_weight'] = weight
                item['exercise_name'] = eblock.xpath('div/strong/span[@class="ename"]/text()').extract()
                item['exercise_category'] = userText.re(r'([a-zA-Z]+)<br>\s*<br>\s*</div>$') or \
                                            items and items[-1]['exercise_category'] or None
                for ex in eblock.xpath('table[@class=""]/tbody'):
                    for load, reps, sets in zip(ex.xpath('tr/td/span[@class="weight n W weightunit-1"]/text()'),
                                                ex.xpath('tr/td/span[@class="n R"]/text()'),
                                                ex.xpath('tr/td/span[@class="n"]/text()')):
                        for _ in xrange(int(sets.extract())):
                            i = item.copy()
                            i['exercise_load'] = load.extract()
                            i['repetitions_done'] = reps.extract()
                            items.append(i)
            self.items.extend(items)

        if self.date < self.date_end:
            self.date += timedelta(days=1)
            return Request(self.start_urls[0] + str(self.date), self.recursive_parse)
        else:
            return self.items

    def parse(self, response):
        if self.date_start == 'today':
            self.date_start = date.today()
        else:
            if not self.date_start:
                self.date_start = response.xpath('//strong[@id="joined"]/text()')[0].extract()
            self.date_start = datetime.strptime(self.date_start, '%Y-%m-%d').date()

        self.date_end = date.today() if self.date_end in ('today', '') else \
                        datetime.strptime(self.date_end, '%Y-%m-%d').date()

        self.date = self.date_start
        return Request(self.start_urls[0] + str(self.date), self.recursive_parse)
