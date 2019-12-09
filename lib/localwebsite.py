import newspaper
from .source import *

class LocalWebsite(Source):
	#########################
	#    URL should be sent as query
	#########################
	async def get_urls(self,query,**kwargs):
	#########################
		#    iterate means some
		#########################
		iterate = int(kwargs.get('iterate',1))
		article_number = iterate 
		html = file_get_contents('../data/data.html')
		bs = BeautifulSoup(html,'lxml')
		a_s = bs.select('a')
		links = []
		for a in a_s:
			try:
				links.append(a['href'])
			except:
				pass
		links = list(set(links))
		return links[0:article_number]