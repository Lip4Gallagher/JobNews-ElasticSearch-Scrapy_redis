# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

# Redis config
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
# 使用 scrapy redis set 去重
# REDIS_START_URLS_AS_SET = True # 加这个参数报错  WRONGTYPE Operation against a key holding the wrong kind of value
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_URL = 'redis://:Mjolnir@127.0.0.1:6379'

#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

# Pipelines config
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300,
    # 'example.pipelines.JsonWriterPipeline': 400,
    'example.pipelines.ElasticSearchPipeline': 500
}

# ElasticSearch config
ELASTICSEARCH_SERVER = 'localhost'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USERNAME = ''
ELASTICSEARCH_PASSWORD = ''
ELASTICSEARCH_INDEX = 'jobnews'
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = 'url'


# Other config
LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 0.05
CONCURRENT_REQUESTS = 800
