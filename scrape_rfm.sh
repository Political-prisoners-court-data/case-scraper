#cd /home/ubuntu/case-scraper && #uncomment before crontab start
bash -c 'http_proxy=http://localhost:4321 https_proxy=http://localhost:4321 \
mamba run -n case-scraper scrapy crawl rfm' &&
mamba run -n case-scraper ./ingest_rfm.py