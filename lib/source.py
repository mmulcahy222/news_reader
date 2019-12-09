import newspaper
import asyncio
import aiohttp
import urllib.parse
import traceback
import concurrent.futures
from bs4 import BeautifulSoup
from collections import Counter
from .helper_functions import *

def catch_exception(func):
	def func_wrapper(self,*args,**kwargs):
		try:
			data = func(self,*args,**kwargs)
			return data
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			exc_text = str(exc_type) + ' ' + str(exc_obj) + ' ' + str(exc_tb.tb_lineno)
			print("Exception for %s ----> %s" % ('',exc_text))
			#
			# MORE DETAILED
			#
			# traceback.print_exc()
			return 'Exception'
	return func_wrapper


class Source():
	def	get_urls(self):
		pass
	#########################
	#    Make synchronous python code asynchronous
	#########################
	async def parse_from_article(self,html):
		article = newspaper.Article('')
		article.is_downloaded = True
		article.set_html(html)
		article.parse()
		text = ''
		#########################
		#    Get Source Url
		#########################
		try:
			locations = []
			bs = BeautifulSoup(html,'lxml')
			for a_el in bs.select('a'):
				href = get_item(a_el.attrs,'href','')
				try:
					locations.append(urllib.parse.urlparse(href)[1])
				except:
					pass
			counter = Counter(locations)
			try:
				source_url = [chunk[0] for chunk in counter.most_common() if len(chunk) > 0][0]
			except:
				source_url = 'exception'
		except:
			# traceback.print_exc()
			source_url = 'undefined'
		#########################
		#    Get Date
		#########################
		try:
			date = article.publish_date.strftime("%B %d %Y")
		except:
			date = ''
		text += " article is from " + source_url + " " + " on " + date + " "
		text += article.title + " "
		article = article.text.replace("&","and").replace('\n','').replace('\t','').replace('.','. ')
		text += article
		return text
	# @catch_exception
	async def get_html(self,url):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					content = await resp.text()
					content = ''.join([x for x in str(content) if ord(x) < 128])
			return content
		except:
			traceback.print_exc()
			return "Time Out or error occured in " + url

	async def facade(self,query,**kwargs):
		tasks = [asyncio.ensure_future(self.get_urls(query,**kwargs))]
		article_urls = await asyncio.gather(*tasks)
		try:
			article_urls = article_urls[0]
		except:
			article_urls = []
		article_urls = list(set(article_urls))
		print("%s articles found" % len(article_urls))
		tasks = [asyncio.ensure_future(self.get_html(url)) for url in article_urls]
		htmls = await asyncio.gather(*tasks)
		print("%s html files retrieved" % len(htmls))
		articles = []
		tasks = [asyncio.ensure_future(self.parse_from_article(html)) for html in htmls]
		articles = await asyncio.gather(*tasks)
		return articles