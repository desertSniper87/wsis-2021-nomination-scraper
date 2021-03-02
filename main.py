from scrapy import cmdline
cmdline.execute("scrapy crawl nominations2 -o nominations2.csv -t csv".split())
