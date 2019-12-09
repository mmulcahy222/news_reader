import lib
from lib import *
from lib.helper_functions import *
import newspaper
import traceback
import concurrent.futures
import urllib.parse
import asyncio
import time
import sys



#########################
#    conversation
#########################
#
query = p("What is the search term?")
type_range = p("""
What is the date range?

1) News
2) News Last 24 Hours
3) News Last Week
4) Search
5) Search Last 24 Hours
6) Search Last Week
7) Website
8) Local Website (at data/data.html)
	""")
page_iterate = int(p("How many articles do you want?"))
os.system("cls")


#########################
#    variables
#########################
rss = lib.rss.Rss()
google = lib.google.Google()
website = lib.website.Website()
local_website = lib.localwebsite.LocalWebsite()
retriever_dict = {
	"1":google,
	"2":google,
	"3":google,
	"4":google,
	"5":google,
	"6":google,
	"7":website,
	"8":local_website
}
type_range_dict = {
	"1":"news",
	"2":"news_today",
	"3":"news_week",
	"4":"search",
	"5":"today",
	"6":"week",
	"7":"website",
	"8":"local_website"
}


#########################
#    Code starts here: Get Articles
#########################
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(retriever_dict[type_range].facade(query,type_range=type_range_dict[type_range],iterate=page_iterate))]
articles = loop.run_until_complete(asyncio.gather(*tasks))
articles = articles[0]
loop.close()

#########################
#    Save Articles In Text File
#########################
file_destination = "C:/makeshift/files/news_reader/text/" + query.replace(" ","_").replace('"','').replace("://","").replace("/",'_') + "_" + time.strftime("%m%d%Y") + ".txt"
with open(file_destination,"a") as f:
	for article in articles:
		article = ''.join([x for x in str(article) if ord(x) < 128])
		print(article)
		print()
		print(article + "\n",file=f)

