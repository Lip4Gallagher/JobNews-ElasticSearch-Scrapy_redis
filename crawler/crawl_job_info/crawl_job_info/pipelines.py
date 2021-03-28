# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from .models4es import JobInfo as Job4ES, index_name


class CrawlJobInfoPipeline(object):
    def process_item(self, item, spider):
        job = Job4ES()
        job.name = item['name']
        job.add_salary(item['salary_max'], item['salary_min'])
        job.pubdate = item['pubdate']
        job.update = item['update']
        job.education = item['education']
        job.experience = item['experience']
        job.company = item['company']
        job.com_logo = item['com_logo']
        job.com_logo_url = item['com_logo_url']
        job.location = item['location']
        job.description = item['description']
        job.add_category(item['main_cate'], item['sub_cate'])
        job.pub_url = item['pub_url']

        if job.save(index=index_name):
            print('Successfully add an item to ElasticSearch.')
        return item
