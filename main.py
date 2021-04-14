from scrapy import cmdline
cmdline.execute("scrapy crawl nominations -o nominations.csv -t csv".split())
