# scrapy_project

# create virtual environment : https://virtualenvwrapper.readthedocs.io/en/latest/install.html (refer)
# clone project : git@github.com:Vishnu-S-S/scrapy_project.git
# install requirements : pip install -r scrapy_project/scrapy_project/scrapy_project/requirements.txt
# create database : https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ (refer)
# run spider : scrapy crawl scrapy_project/scrapy_project/scrapy_project/spiders/flipkart_spider.py
# arguments passing : 1. -a pages=2 (hint: for stop the script after scraping two pages, optional)
#                     2. -o raw_file.jl (hint: to write the json data scraped into a file for verifying)
# shell commands for view data stored in mongodb:
#                     $ mongo
#                     $ use scrapy_project
#                     $ db.items.find()
# Also use any third party apllication for view data from mongodb (eg: robo3T)
