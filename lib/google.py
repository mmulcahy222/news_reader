import newspaper
import urllib.parse
from bs4 import BeautifulSoup
from .source import *
from .helper_functions import *
import itertools
import asyncio
import aiohttp 

class Google(Source):

	async def get_urls_in_single_page(self,query,offset,type_range):
		query = urllib.parse.quote(query)
		url = 'https://www.google.com/search?start='+str(offset)+'&q=' + str(query)
		google_interval = 10
		text = ''
		if type_range == 'today':
			url += 'tbs=qdr:d'
		if type_range == 'week':
			url += '&tbs=qdr:w'
		if type_range == 'news':
			url += '&tbm=nws'
		if type_range == 'news_today':
			url += '&tbm=nws&tbs=qdr:d'
		if type_range == 'news_week':
			url += '&tbm=nws&tbs=qdr:w'
		html = get_html(url)
		bs = BeautifulSoup(html,"lxml")
		return [a.attrs['href'] for a in bs.select(".dbsr a") if 'http' in a.attrs['href']]
	#########################
	#    iterate=2, type_range="news_today"
	#########################
	async def get_urls(self,query,**kwargs):
		type_range = kwargs.get('type_range')
		iterate = kwargs.get('iterate',1)
		google_interval = 10
		# tasks = [asyncio.ensure_future(self.get_urls_in_single_page(query,offset,type_range)) for offset in range(0,google_interval*iterate,google_interval)]
		tasks = [asyncio.ensure_future(self.get_urls_in_single_page(query,offset,type_range)) for offset in range(0,iterate,google_interval)]
		image_links = await asyncio.gather(*tasks)
		image_links = list(itertools.chain.from_iterable(image_links))
		return image_links
	