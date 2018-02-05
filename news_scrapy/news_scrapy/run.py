# coding:utf-8

from scrapy import cmdline
# cmdline.execute("scrapy crawl sina_news".split())
cmdline.execute("scrapy crawl ifeng_news -o out.json -t json".split())