# Scrapy settings for hindu_tamil project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hindu_tamil'

SPIDER_MODULES = ['hindu_tamil.spiders']
NEWSPIDER_MODULE = 'hindu_tamil.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hindu_tamil (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#    'hindu_tamil.middlewares.Hindu_TamilSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'hindu_tamil.middlewares.Hindu_TamilDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'hindu_tamil.pipelines.Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 1000

HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.DbmCacheStorage'


CHCHCH_DIR     = '/home/vanangamudi/agam/projects/code/tamilnlp/indraya-kiruvam/'

DATA_DIR       = '{}/data/extract'.format(CHCHCH_DIR)
DELTAFETCH_DIR = '{}/data/deltafetch/hindu_tamil'.format(CHCHCH_DIR)
HTTPCACHE_DIR  = '{}/data/httpcache/hindu_tamil'.format(CHCHCH_DIR)

# run like  -- scrapy crawl hindu_tamil -s JOBDIR='CHCHCH_DIR/jobs/hindu_tamil
DEPTH_PRIORITY = 1 
SCHEDULER_DISK_QUEUE   = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

#https://stackoverflow.com/a/39173768
"""
Currently Scrapy does DNS resolution in a blocking way with usage of thread pool. With higher concurrency levels the crawling could be slow or even fail hitting DNS resolver timeouts. Possible solution to increase the number of threads handling DNS queries. The DNS queue will be processed faster speeding up establishing of connection and crawling overall.
"""
REACTOR_THREADPOOL_MAXSIZE = 20

#deltafetch
# install libdb-dev
# pip install scrapy-deltafetch
# scrapy crawl example -a deltafetch_reset=1
SPIDER_MIDDLEWARES['scrapy_deltafetch.DeltaFetch'] = 100
DELTAFETCH_ENABLED = True


# MongoDB to store the scraped data
MONGODB_SERVER     = "localhost"
MONGODB_PORT       = 27017

MONGODB_DB         = "test"
MONGODB_COLLECTION = "kiruvam"
