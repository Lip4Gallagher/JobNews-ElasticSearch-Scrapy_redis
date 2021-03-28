import json
import pathlib
import re
import uuid
from urllib.parse import urljoin, urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from ..items import JobInfoItem


class ChitoneSpider(RedisCrawlSpider):
    name = 'chitone'
    # redis_key = '{}:start_urls'.format(name)
    allowed_domains = ['job5156.com']

    rules = [
        Rule(LinkExtractor(allow=r'https://www.job5156.com/index/zhaopin_[\S]+'), follow=True),
        Rule(LinkExtractor(allow=r'https://www.job5156.com/[\S]+\/job_[0-9]+'), callback='parse_job_info', follow=False)
    ]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def parse_job_info(self, response):
        job_item = JobInfoItem()
        job_item['name'] = response.xpath('//h1[@class="pos_name"]/text()').extract_first()
        salary = response.xpath('//h1[@class="pos_name"]/following-sibling::span/text()').get('0-0').split('-')
        no_unit = True
        try:
            int(salary[0])
        except ValueError:
            try:
                float(salary[0])
            except ValueError:
                no_unit = False

        job_item['salary_max'] = salary[1]
        unit = ''.join(re.findall(r'\D', job_item['salary_max'])).replace('.', '')
        if no_unit:
            job_item['salary_min'] = ''.join([salary[0], unit])
        content_str = response.xpath('//script[contains(text(),"pubDate")]/text()').get()
        content_dic = json.loads(content_str)
        if content_dic:
            job_item['pubdate'] = content_dic.get('pubDate', None)
            job_item['update'] = content_dic.get('upDate', None)
            job_item['description'] = content_dic.get('description', None)

        job_item['education'] = response.xpath('//ul[@class="requirements"]/li[1]/p/text()').extract_first()
        job_item['experience'] = response.xpath('//ul[@class="requirements"]/li[2]/p/text()').extract_first()
        job_item['company'] = response.xpath('//div[@class="com_msg02_content"]/ul/li[1]/strong/text()').extract_first()
        com_logo = response.xpath('//img[@class="com-logo"]/@src').extract_first()
        logo_url = urljoin(response.url, com_logo)
        job_item['com_logo_url'] = logo_url
        job_item['location'] = response.xpath('//ul[@class="requirements"]/li[3]/p/text()').extract_first()
        job_item['main_cate'] = response.xpath('//*[@class="crumbs_cont"]//p[1]/a[2]/text()').get()
        job_item['sub_cate'] = response.xpath('//*[@class="crumbs_cont"]//p[1]/a[3]/text()').get()
        job_item['pub_url'] = response.url
        yield scrapy.Request(
            url=logo_url,
            callback=self.download_logo,
            meta={'item': job_item}
        )

    def download_logo(self, response):
        image_path = self.settings.get('IMAGE_PATH')
        if not image_path.is_dir():
            image_path.mkdir(parents=True, exist_ok=True)

        com_logo = image_path.joinpath('{}{}'.format(
            str(uuid.uuid4()), pathlib.Path(urlparse(response.url).path).suffix)
        )
        with com_logo.open('wb+') as fh:
            fh.write(response.body)

        item = response.meta.get('item')
        item['com_logo'] = str(com_logo)
        yield item
