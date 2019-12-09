import newspaper
from .source import *

class Website(Source):
	#########################
	#    URL should be sent as query
	#########################
	async def get_urls(self,query,**kwargs):
	#########################
		#    iterate means some
		#########################
		iterate = int(kwargs.get('iterate',1))
		article_number = iterate
		url = query
		if 'url'.startswith('http') == False:
			url = 'http://' + url
		url = url.replace("www.",'')
		build = newspaper.build(url, memoize_articles=False)
		build.download()
		articles = build.articles
		article_links = []
		for article in articles:
			article_links.append(article.url)
		return article_links[0:article_number]